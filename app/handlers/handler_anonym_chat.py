# -*- coding: utf-8 -*-


# Импорт необходимых модулей.
from loguru import logger

from typing import Dict, Any

from aiogram import Router, F
from aiogram.types import Message

from app.data_base.requests import MyRequests
from app.bot_settings import bot
from app.middlewares.chat_middleware import ChatMiddleware
from app.keyboards.keyboards import *


# Инициализация роутера.
router = Router(name=__name__)


# Подключение middleware.
router.message.middleware(ChatMiddleware())


# Обработчик завершения диалога.
@router.message(F.text == 'Стоп ❌')
async def stop_dialog(message: Message, info: Dict[str, Any]) -> None:
    """Завершает диалог пользователя, если тот ведет диалог с кем-либо"""

    user_id = message.from_user.id
    companion_id = info['companion']

    try:
        for user in [user_id, companion_id]:
            await bot.send_message(
                chat_id=user,
                text=f'❗️<b>Диалог завершен</b>\n\n'
                     f'Вы отправили <ins>{info['messages']}</ins> сообщений! 💬\n\n',
                reply_markup=MainMenu(1),
            )

            await MyRequests.delete_line('Dialogs', 'user_1', user_id) or await MyRequests.get_line('Dialogs', 'user_2', user_id)

    except Exception as e:
        logger.error(f'An error has occurred {e}')


# Обработчик текстовых сообщений от пользователей.
@router.message()
async def send_message(message: Message, info: Dict[str, Any]) -> None:
    """Пересылает сообщение пользователя своему собеседнику, если тот ведет диалог с кем-либо. """

    user_id = message.from_user.id
    content = message.text
    companion = info['companion']

    try:
        await MyRequests.add_items('Dialogs', messages=info['messages'] + 1)

        await bot.send_message(
            chat_id=companion,
            text=content,
        )

        logger.info(
            f'Пользователь {user_id} отправил сообщение "{content}" пользователю {companion}\n\n'
        )
    except Exception as e:
        logger.error(f'An error has occurred {e}')
