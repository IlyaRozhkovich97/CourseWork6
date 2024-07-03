from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView
from django.contrib import messages
from .forms import UserRegisterForm, UserProfileForm, CustomAuthenticationForm
from .models import User
from .utils import generate_token, generate_password
from django.contrib.auth.views import LoginView


# Класс для регистрации новых пользователей
class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        token = generate_token()
        form.instance.token = token
        user = form.save()
        user.email_user(
            subject='Верификация почты',
            message=f'Поздравляем с регистрацией на iStore \n'
                    f'Для подтверждения регистрации перейдите по ссылке: \n'
                    f'http://127.0.0.1:8000/users/confirm/{user.token} \n'
                    f'Если вы не причастны к регистрации игнорируйте это письмо.'
        )
        return super().form_valid(form)


# Функция для верификации пользователя по токену
def verify_view(request, token):
    user = get_object_or_404(User, token=token)
    user.is_verified = True
    user.save()
    return render(request, 'users/verify.html')


# Функция для сброса пароля
def res_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()
        if user:
            new_password = generate_password()
            user.email_user(
                subject='Смена пароля',
                message=f'Ваш новый пароль {new_password}'
            )
            user.set_password(new_password)
            user.save()
        else:
            messages.error(request, 'Пользователь не найден.')
        return redirect(reverse('users:reset_password'))
    return render(request, 'users/reset_password.html')


# Класс для обновления профиля пользователя
class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


# Класс для обработки входа пользователя в систему
class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'users/login.html'
