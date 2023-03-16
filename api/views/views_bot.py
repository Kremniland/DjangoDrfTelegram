import pdb
from pprint import pprint
from loguru import logger

from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from rest_framework import viewsets

from api.serializers.serializers_bot import UserTgSerializer, MessageSerializer
from src.telegram.models import UserTg, Message


User = get_user_model()


@extend_schema_view(
    list=extend_schema(summary='Просмотр', tags=['Пользователи телеграмма']),
    retrieve=extend_schema(summary='Просмотр', tags=['Пользователи телеграмма']),
    create=extend_schema(summary='Создание', tags=['Пользователи телеграмма']),
    partial_update=extend_schema(summary='Редактирование частично', tags=['Пользователи телеграмма']),
    update=extend_schema(summary='Редактирование', tags=['Пользователи телеграмма']),
    destroy=extend_schema(summary='Удаление', tags=['Пользователи телеграмма']),
)
class UserTgView(viewsets.ModelViewSet):
    queryset = UserTg.objects.all()
    serializer_class = UserTgSerializer
    # permission_classes = (IsAuthenticated,)
    # authentication_classes = (TokenAuthentication,)


@extend_schema_view(
    get=extend_schema(summary='Сообщения', tags=['Сообщения телеграмма']),
)
class MessageView(generics.ListAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


    def get_queryset(self):
        user_id = self.kwargs.get('pk')
        if user_id:
            return Message.objects.filter(user_id=user_id).select_related('user_id')
        return Message.objects.all().select_related('user_id')


