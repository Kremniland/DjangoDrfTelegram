from django.contrib import admin

from src.telegram.models import UserTg, Message
from .forms import MessageForm


@admin.register(UserTg)
class UserTgAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_tg_id', 'first_name', 'username', 'create_date')
    list_display_links = ('id', 'user_tg_id', 'first_name', 'username', )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'chat_id', 'create_date',)
    list_display_links = ('id', 'user_id', 'chat_id',)
    form = MessageForm # собственная фора

    
