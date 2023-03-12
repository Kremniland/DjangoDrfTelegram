from django.contrib.auth.base_user import BaseUserManager
from rest_framework.exceptions import ParseError

class CustomUserManager(BaseUserManager):
    use_in_migrations = True # чтобы проходили миграции

    def _create_user(self, phone_number=None, username=None, email=None, password=None, **extra_fields):
        if not (email or phone_number or username): # что то из этого должно быть при регистрации
            raise ParseError('Укажите email или телефон')

        if email:
            email = self.normalize_email(email) # проверяем, нормализуем емаил

        if not username:
            if email:
                username = email.split('@')[0]
            else:
                username = phone_number

        user = self.model(username=username, **extra_fields) # создаем объект класса и передаем **extra_fields
        user.email = email # присваиваем полю емаил принятый емаил
        user.set_password(password) # сохраняем пароль в зашифрованном виде
        user.save(using=self._db) # сохраняем созданного юзера
        return user

    def create_user(self, phone_number=None, email=None, password=None, username=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_active', True)

        return self._create_user(
            phone_number, email, password, username, **extra_fields
        )

    def create_superuser(self, phone_number=None, email=None, password=None, username=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        return self._create_user(
            phone_number, email, password, username, **extra_fields
        )





