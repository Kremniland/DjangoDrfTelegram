from aiogram import Bot, Dispatcher

from telegramm_bot.config import TOKEN
from telegramm_bot.bot_utils import handlers

bot = Bot(TOKEN)
dp = Dispatcher(bot)

dp.register_message_handler(handlers.start_cmd, commands='start')


if __name__ == '__main__':
    pass
