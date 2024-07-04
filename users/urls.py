from django.contrib.auth.views import LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterView, ProfileView, verify_view, res_password, UserListView, toggle_activity
from .views import CustomLoginView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('confirm/<token>/', verify_view, name='verify_success'),
    path('password/reset/', res_password, name='reset_password'),
    path('users_list/', UserListView.as_view(), name='users_list'),
    path('toggle_activity/<int:pk>/', toggle_activity, name='toggle_activity')
]
