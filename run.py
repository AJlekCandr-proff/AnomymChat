# -*- coding: utf-8 -*-


# Импорт необходимых модулей.
import asyncio

from loguru import logger

from aiogram import Dispatcher, Bot

from app.bot_settings import bot
from app.handlers import router as main_handlers_router
from app.data_base.Engine import async_engine


# Настройка логирования
logger.add("bot.logs.txt", rotation="1 MB", level="INFO", format="{time} {level} {message}")


# Функция запуска бота.
async def main_func(main_bot: Bot) -> None:
    """Запускает бота и обновляет базу данных. """

    dp = Dispatcher()

    dp.include_routers(
        main_handlers_router,
    )

    try:
        logger.info('Bot successfully started!')
        await async_engine()
        await dp.start_polling(main_bot)

    except Exception as e:
        logger.error(f'An error has occurred: {e}')
    finally:
        logger.info('Bot successfully finished!')
        await main_bot.session.close()


# Конструкция __name__ == '__main__'.
if __name__ == '__main__':

    # Запуск бота.
    asyncio.run(main_func(bot))
