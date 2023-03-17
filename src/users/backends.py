from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()


class AuthBackend(object):
    '''Позврляет изменить авторизацию на самом низком уровне с любой аторизацией
    Можно вместо username вводить емаил, имя или номер телефона'''
    supports_object_permissions = True # поддержка пермишинов на уровне объектов модели
    supports_anonymous_user = True # False - выключение могут ли логиниться анонимные пользователи
    supports_inactive_user = True # False - не авторизуем не активных пользователей

    def get_user(self, user_id):
        '''служебный метод без которого не будет работать данный backend'''
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def authenticate(self, request, username, password):
        '''Проверяем username полям username, email, phone_number а не только по username
        и проверяем правильно ли пользователь ввел пароль'''
        try:
            user = User.objects.get(
                Q(username=username) |
                Q(email=username) |
                Q(phone_number=username)
            )
        except User.DoesNotExist:
            return None
        return user if user.check_password(password) else None # правильно ли пользователь ввел пароль
