import pdb
from pprint import pprint
from loguru import logger

from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from src.users.serializers.api.users import (
    RegistrationSerializer, ChangePasswordSerializer, MeSerializer, MeUpdateSerializer)

User = get_user_model()


@extend_schema_view(
    post=extend_schema(summary='Регистрация', tags=['Аутентификация и регистрация']),
)
class RegistrationView(generics.CreateAPIView):
    '''регистрация пользователя'''

    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer


@extend_schema_view(
    post=extend_schema(
        request=ChangePasswordSerializer,  # что бы в документации было видно какие данные мы ожидаем
        summary='Смена пароля', tags=['Аутентификация и регистрация']),
)
class ChangePasswordView(APIView):
    '''Изменение пароля пользователя'''

    def post(self, request):
        logger.info(request.__dict__)
        user = request.user
        serializer = ChangePasswordSerializer(
            instance=user, data=request.data
        )
        # pdb.set_trace()
        logger.info(self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=HTTP_204_NO_CONTENT)


@extend_schema_view(
    get=extend_schema(summary='профиль пользователя', tags=['Пользователи']),
    put=extend_schema(summary='изменить профиль пользователя', tags=['Пользователи']),
    patch=extend_schema(summary='изменить частично профиль пользователя', tags=['Пользователи']),
)
class MeView(generics.RetrieveUpdateAPIView):
    '''что бы в запросе не отправлять pk переопределяем метод get_object
    и ставим pk=self.request.user, переопределяем get_serializer_class для использования
    разных сериализаторов под разные методы запросов GET, PUT, PATCH'''

    queryset = User.objects.all()
    serializer_class = MeSerializer

    def get_serializer_class(self):
        '''переопределяем get_serializer_class для использования
        разных сериализаторов под разные методы запросов GET, PUT, PATCH'''
        logger.info(self.request.__dict__)
        if self.request.method in ['PUT', 'PATCH']:
            return MeUpdateSerializer
        return MeSerializer

    def get_object(self):
        '''что бы в запросе не отправлять pk переопределяем метод get_object
        и ставим pk=self.request.user'''
        return self.request.user
