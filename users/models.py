from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель для пользователя"""
    USER = 'пользователь'
    ADMIN = 'администратор'

    ROLE_CHOICES = (
        (USER, 'пользователь'),
        (ADMIN, 'администратор'),
    )

    username = None
    email = models.EmailField(unique=True, verbose_name='почта')
    phone = models.CharField(max_length=20, verbose_name='телефон', blank=True, null=True)
    role = models.CharField(max_length=20, verbose_name='роль', choices=ROLE_CHOICES, default=USER)
    image = models.ImageField(upload_to='', verbose_name='аватар', blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f'{self.email}'
