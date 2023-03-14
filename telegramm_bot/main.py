from aiogram import executor

from telegramm_bot.bot_utils.bot_routers import dp


if __name__ == '__main__':
    executor.start_polling(dp,
                           skip_updates=True)