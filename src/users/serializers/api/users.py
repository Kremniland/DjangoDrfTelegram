from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.exceptions import ParseError


User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):

    email = serializers.EmailField()
    # значит поле доступно для записи и в ответ при регистрации нам не придет наш пароль
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'password',) # ID не будет в запросе т к изначально оно ридонли

    def validate_email(self, value):
        email = value.lower()
        if User.objects.filter(email=email).exists():
            raise ParseError(
                'Такая почта уже существует'
            )
        return email

    def validate_password(self, value):
        validate_password(value)
        return value


