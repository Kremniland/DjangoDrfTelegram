import aiohttp
from aiogram import types, Dispatcher, Bot
from asgiref.sync import async_to_sync, sync_to_async
from loguru import logger
from django.conf import settings

from src.telegram.bot_utils.services import (
    add_user_message, get_all_message, registration_user_django, get_auth_token)
from src.telegram.models import UserTg, Message


bot = Bot(settings.TOKEN)
dp = Dispatcher(bot)


async def start_cmd(message: types.Message):
    # await add_user(message)
    # res = await get_user_all()
    await add_user_message(message)
    await bot.send_message(chat_id=message.chat.id, text=f'Good!')


async def get_message(message: types.Message):
    await add_user_message(message)
    res = await get_all_message()
    logger.info(res)
    await message.answer('OK!')


async def reg_user(message: types.Message):
    await add_user_message(message)
    await registration_user_django(first_name='name1312', last_name='name112', email='ema11i3l2@email.ru', password='1234')
    await message.answer('Ok!')


async def token(message: types.Message):
    await add_user_message(message)
    auth_token = await get_auth_token(username="admin", password="1234")
    token = auth_token.split('"')[3]
    logger.info(token)
    await message.reply(f'Token: {token}')

