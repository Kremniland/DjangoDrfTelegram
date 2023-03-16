import aiohttp
from aiogram import types
from asgiref.sync import async_to_sync, sync_to_async
from loguru import logger

from src.telegram.bot_utils.services import (
    add_user_message, get_all_message, registration_user_django, get_auth_token)
from src.telegram.models import UserTg, Message


async def start_cmd(message: types.Message):
    # await add_user(message)
    # res = await get_user_all()
    await add_user_message(message)
    await message.answer(f'Good!')


async def get_message(message: types.Message):
    res = await get_all_message()
    logger.info(res)
    await message.answer('OK!')


async def reg_user(message: types.Message):
    await registration_user_django(first_name='name1312', last_name='name112', email='ema11i3l2@email.ru', password='1234')
    await message.answer('Ok!')


async def token(message: types.Message):
    auth_token = await get_auth_token(username="admin", password="1234")
    logger.info(auth_token)
    await message.reply('Ok!')
