from aiogram import types
from asgiref.sync import async_to_sync, sync_to_async
from loguru import logger

from src.telegram.models import UserTg, Message


async def add_user(message):
    '''пример сохранения пользователя в базу если его там нет async методом aget_or_create'''
    user_tg_id = message.from_user.id
    r = await UserTg.objects.aget_or_create(
                user_tg_id=user_tg_id,
                defaults={
                    'first_name': message.from_user.first_name,
                    'username': message.from_user.username,
                }
            )
    logger.info(r)


@sync_to_async()
def add_user_message(message: types.Message):
    '''проверяем если пользователя нет в базе то создаем юзера
        далее сохраняем его сообщение'''
    user_tg_id = message.from_user.id
    user, boole = UserTg.objects.get_or_create(
                user_tg_id=user_tg_id,
                defaults={
                    'first_name': message.from_user.first_name,
                    'username': message.from_user.username,
                }
            )
    logger.info(user)
    Message(
        user_id=user,
        chat_id=message.chat.id,
        text=message.text
    ).save()
    mes = Message.objects.filter(user_id=user).first()
    logger.info(mes.user_id.username)
