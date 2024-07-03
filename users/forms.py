from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from users.models import User
from django.forms import ModelForm, BooleanField
from django import forms
from django.contrib.auth.forms import AuthenticationForm


class StyleFormMixin(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class UserRegisterForm(UserCreationForm, StyleFormMixin):
    class Meta:
        model = User
        fields = (
            "email", "nickname", "first_name", "last_name", "phone", "country", "avatar", "password1", "password2")


class UserProfileForm(UserChangeForm, StyleFormMixin):
    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "phone", "country", "avatar")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
