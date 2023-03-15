from aiogram import types
from asgiref.sync import async_to_sync, sync_to_async
from loguru import logger

from src.telegram.bot_utils.services import add_user_message
from src.telegram.models import UserTg, Message


async def start_cmd(message: types.Message):
    # await add_user(message)
    # res = await get_user_all()
    await add_user_message(message)
    await message.answer(f'Good!')
