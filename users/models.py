from django.db import models
from django.contrib.auth.models import AbstractUser
from catalog.models import NULLABLE


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')
    phone = models.CharField(max_length=35, verbose_name='телефон', **NULLABLE)
    avatar = models.ImageField(upload_to='users/', verbose_name='аватар', **NULLABLE)
    country = models.CharField(max_length=50, verbose_name='страна', **NULLABLE)
    is_verified = models.BooleanField(default=False, verbose_name='Подтверждён')
    token = models.CharField(max_length=10, verbose_name='Токен', **NULLABLE)
    nickname = models.CharField(max_length=50, verbose_name='никнейм', unique=True, **NULLABLE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email
