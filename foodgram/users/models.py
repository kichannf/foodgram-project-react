from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(
        'Логин',
        max_length=150,
        unique=True,
    )
    password = models.CharField(
        'Пароль',
        max_length=150,
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
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
    )

    class Meta:
        ordering = ('username',)

    def __str__(self):
        return self.username


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        verbose_name='Подписчик',
        related_name='follower',
        on_delete=models.CASCADE
    )
    following = models.ForeignKey(
        User,
        verbose_name='Автор',
        related_name='following',
        on_delete=models.CASCADE
    )

    class Meta:
        constraints = (
            models.UniqueConstraint(
                fields=('user', 'following',),
                name='unique_user'
            ),
        )
