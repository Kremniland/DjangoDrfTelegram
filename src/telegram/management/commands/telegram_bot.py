from aiogram import Bot, Dispatcher, executor
from django.conf import settings
from django.core.management.base import BaseCommand

from src.telegram.bot_utils.handlers import start_cmd


bot = Bot(settings.TOKEN)
dp = Dispatcher(bot)


dp.register_message_handler(start_cmd, )


class Command(BaseCommand):
    help = 'Телеграм Бот'

    def handle(self, *args, **options):
        executor.start_polling(dp,
                               skip_updates=True)





