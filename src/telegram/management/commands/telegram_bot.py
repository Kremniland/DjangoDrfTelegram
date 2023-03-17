from aiogram import Bot, Dispatcher, executor
from django.conf import settings
from django.core.management.base import BaseCommand

from src.telegram.bot_utils.handlers import dp, start_cmd, get_message, reg_user, token


# bot = Bot(settings.TOKEN)
# dp = Dispatcher(bot)

dp.register_message_handler(get_message, commands='message')
dp.register_message_handler(reg_user, commands='reg_user')
dp.register_message_handler(token, commands='token')
dp.register_message_handler(start_cmd, )


class Command(BaseCommand):
    help = 'Телеграм Бот'

    def handle(self, *args, **options):
        executor.start_polling(dp,
                               skip_updates=True)





