from django.contrib.auth.models import AbstractUser
from django.db import models

from foodgram.settings import ROLE_CHOICES


class User(AbstractUser):
    username = models.CharField(
        'Логин',
        max_length=150,
        unique=True,
    )
    password = models.CharField(
        'Пароль',
        max_length=150,
        blank=True,
    )
    email = models.EmailField(
        'email',
        max_length=254,
        help_text='Электронная почта',
        unique=True,
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank=True,
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=True,
    )
    role = models.TextField(
        'Роль',
        choices=ROLE_CHOICES,
        default='user',
        help_text='Роль пользователя',
    )

    class Meta:
        ordering = ('username',)

    def __str__(self):
        return self.username
