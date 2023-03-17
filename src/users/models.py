from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models

from .managers import CustomUserManager


class User(AbstractUser):
    # username = None # уберет вообще это поле, только тогда надо будет удалить его в CustomManagere везде
    username = models.CharField(
        max_length=64, unique=True, null=True, blank=True, verbose_name='Никнейм'
    ) # делаем поле уникальным для выбора поля для логина
    email = models.EmailField(unique=True, null=True, blank=True, verbose_name='Почта') # делаем поле уникальным для выбора поля для логина
    phone_number = PhoneNumberField(null=True, blank=True, unique=True, verbose_name='Телефон') # делаем поле уникальным для выбора поля для логина
    tg_user_id = models.IntegerField(null=True, blank=True, verbose_name='Телеграм ID')
    avatar = models.ImageField(upload_to='image/avatar_user/', null=True, blank=True, verbose_name='Фотография')

    is_verified = models.BooleanField(default=False, verbose_name='Верификация')

    USERNAME_FIELD = 'username' # поле должно быть уникальным какое поле используется логин по умолчанию username
                                # но так прописали backends то username проверяется по  username, mail, phone_number
    # REQUIRED_FIELDS = [] # обязательные поля

    objects = CustomUserManager() # переопределяем менеджер на свой

    class Meta:
        db_table = 'user'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        unique_together = ('username', 'email',) # делаем уникальный составной ключ

    @property # можем обратиться к full_name но в модели его не будет
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return f'{self.full_name} ({self.pk})'


class Profile(models.Model):
    GENDER = [
        ('Man', 'Man'),
        ('Woman', 'Woman'),
    ]
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='profile',
        verbose_name='Пользователь')
    gender = models.CharField(max_length=6, choices=GENDER, default='Man', verbose_name='Пол')
    info = models.CharField(max_length=512, verbose_name='Информация')

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'

    def __str__(self):
        return f'{self.user} ({self.pk})'




