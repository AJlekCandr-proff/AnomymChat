# -*- coding: utf-8 -*-


# Импорт необходимых модулей.
from loguru import logger

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from app.data_base.requests import MyRequests
from app.keyboards.keyboards import MainMenu


# Инициализация роутера.
router = Router(name=__name__)


# Обработчик команды /start.
@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    """Присылает приветствие и меню для пользователя и добавляет его в базу данных. """

    user_id = message.from_user.id
    full_name = message.from_user.full_name

    try:
        await message.answer(
            text='👋 <i>Привет! Это Анонимный чат Telegram.</i>\n'
                 '<i>Тут можно общаться 1 на 1 со случайными собеседниками 💬</i>\n\n'
                 '📖 <i>В чате есть правила поведения, которые нужно соблюдать.</i>\n'
                 '<i>Нельзя спамить, продвигать свои услуги, оскорблять собеседников.</i>\n\n'
                 '<i>Удачного общения! Будьте вежливы к собеседникам ❤️</i>\n\n'
                 '<b>Скорее начинай общение 👇🏻</b>',
            reply_markup=MainMenu(2),
        )
        await MyRequests.add_items('Users', user_id=user_id, full_name=full_name)

        logger.info(f'Пользователь {user_id} запустил бота!')

    except Exception as e:
        logger.error(f'An error has occurred {e}')
