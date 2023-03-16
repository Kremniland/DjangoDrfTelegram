import aiohttp
from aiogram import types
from asgiref.sync import async_to_sync, sync_to_async
from loguru import logger

from src.telegram.models import UserTg, Message


async def async_add_user(message):
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


async def get_auth_token(username: str, password: str):
    '''получение токена'''
    data = {
        "password": password,
        "username": username
    }
    async with aiohttp.ClientSession() as session:
        resp = await session.post(url='http://127.0.0.1:8000/djoser/token/login/', data=data)
        auth_token = await resp.text()
        logger.info(auth_token)
        return auth_token


async def get_all_message():
    '''делает GET запрос на эндпоинт и возвращает весь список сообщений в Jsson формате'''
    headers = {'Authorization': 'Token 04a122ce0a2f8b8d2634f85016946df919d6b19b'}
    async with aiohttp.ClientSession() as session:
        async with session.get(url='http://127.0.0.1:8000/api/message/', headers=headers) as response:
            logger.info(response)
            return await response.json()


async def registration_user_django(first_name: str, last_name: str, email: str, password: str):
    '''регистрация пользователя Django'''
    data = {"first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password
            }
    async with aiohttp.ClientSession() as session:
        res = await session.post(url='http://127.0.0.1:8000/users/users/reg/',
                                 data=data)
        logger.info(res.status)


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
