from rest_framework import serializers
from django.contrib.auth import get_user_model

from src.telegram.models import UserTg, Message


User = get_user_model()


class UserTgShotSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTg
        fields = ('id', 'user_tg_id', 'first_name', 'username',)


class UserTgSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTg
        fields = ('id', 'user_tg_id', 'first_name', 'username', 'create_date')


class MessageSerializer(serializers.ModelSerializer):
    # user_id = serializers.StringRelatedField(many=False, read_only=True)
    user_id = UserTgShotSerializer()

    class Meta:

        model = Message
        fields = ('id', 'text', 'chat_id', 'create_date', 'user_id')

