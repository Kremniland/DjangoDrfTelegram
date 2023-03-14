from aiogram import types


async def start_cmd(message: types.Message):
    await message.answer('Hello!')