from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework.exceptions import ValidationError


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('username', 'first_name', 'last_name')
    email = models.EmailField(
        'email',
        max_length=254,
        help_text='Электронная почта',
        unique=True,
    )

    class Meta:
        ordering = ('id',)

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
                name='unique_follow'
            ),
        )

    def clean(self):
        if self.user == self.following:
            raise ValidationError('Нельзя подписаться на самого себя')

    def __str__(self):
        return f'{self.user} подписан на {self.following}'
