from aiogram import Bot, Dispatcher, executor, types
from django.conf import settings
from django.core.management.base import BaseCommand
from asgiref.sync import async_to_sync, sync_to_async
from loguru import logger

from src.telegram.models import UserTg, Message


bot = Bot(settings.TOKEN)
dp = Dispatcher(bot)


async def add_user(message):
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


@dp.message_handler()
async def start_cmd(message: types.Message):
    # await add_user(message)
    # res = await get_user_all()
    await add_user_message(message)
    await message.answer(f'Good!')


class Command(BaseCommand):
    help = 'Телеграм Бот'

    def handle(self, *args, **options):
        executor.start_polling(dp,
                               skip_updates=True)





