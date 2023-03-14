from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ParseError
from loguru import logger

from src.users.models import Profile

User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    '''для модели Profile'''

    class Meta:
        model = Profile
        fields = (
            'gender', 'info',
        )


class RegistrationSerializer(serializers.ModelSerializer):
    '''регистрация пользователя'''
    email = serializers.EmailField()
    # переопределяем поле password  write_only=True чтобы поле
    # с паролем не возвращалось при ответе, что бы не было его видно
    password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True
    )

    class Meta:
        model = User
        fields = (
            'id', 'first_name', 'last_name', 'email', 'password',
        )  # ID не будет в запросе т к изначально оно ридонли

    def validate_email(self, value):
        email = value.lower()
        if User.objects.filter(email=email).exists():
            raise ParseError(
                'Такая почта уже существует'
            )
        return email

    def validate_password(self, value):
        '''простая валидация пароля не короткий не легкий и т д как в сеттингах'''
        validate_password(value)
        return value

    def create(self, validated_data):
        '''захэширует пароль в базе'''
        # create_user встроенная ф-ия которая при сохранении нового пользователя
        # пароль в базе сохранит хэшом
        user = User.objects.create_user(**validated_data)
        return user


class ChangePasswordSerializer(serializers.ModelSerializer):
    '''изменение пароля'''
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'old_password', 'new_password',
        )

    def validate(self, attrs):
        '''делаем валидацию для проверки старого пароля введенного для юзера'''
        user = self.instance  # берем из instance user
        old_password = attrs.pop('old_password')  # берем из переданных аттрибутов old_password
        if not user.check_password(old_password):  # встроенная функция проверяет пароль юзера с переданным нами паролем
            raise ParseError(
                'Старый пароль не верный'
            )
        return attrs

    def validate_new_password(self, value):
        '''простая валидация пароля не короткий не легкий и т д как в сеттингах'''
        validate_password(value)
        return value

    def update(self, instance, validate_data):
        '''переопределяем для сохранения введенных данных
        instance - это наш пользователь
        validate_data=attrs из ф-ии validate'''
        password = validate_data.pop('new_password')
        instance.set_password(password)  # встроенная ф-ия помещает пароль в пароль юзера
        instance.save()  # сохраняем изменения
        return instance


class MeSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = (
            'id', 'username', 'first_name', 'last_name', 'email', 'tg_user_id', 'phone_number',
            'profile', 'date_joined',
        )


class MeUpdateSerializer(serializers.ModelSerializer):
    '''Изменение данных пользователя, что бы изменить и поля профиля переопределяем
    метод update'''
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = (
            'id', 'username', 'first_name', 'last_name', 'email', 'tg_user_id',
            'phone_number', 'profile',
        )

    def update(self, instance, validated_data):
        # проверка наличие данных для изменения в модели profile в запросе на изменение
        # if 'profile' in validated_data:
        #     profile_data = validated_data.pop('profile')  # забираем из входящих данных профиль
        # else:
        #     profile_data = None  # если профиля нет в запросе на изменение
        # == тоже самое ===
        logger.info(instance.__dict__)
        profile_data = validated_data.pop('profile') if 'profile' in validated_data else None

        # сохраняем изменения данных в модели юзера instance - пользователь, validated_data - данные для изменения
        instance = super().update(instance, validated_data)

        if profile_data:  # сохраняем изменения в модели профиле если данные для изменения есть
            profile = instance.profile
            for key, value in profile_data.items():  # проходим по данным для изменения профиля
                if hasattr(profile, key):  # если в профиле есть такой ключ
                    setattr(profile, key, value)  # сохраняем ключ значение полученные для изменения в модели профиля
            profile.save()
        return instance
