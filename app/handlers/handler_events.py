# -*- coding: utf-8 -*-


# Импорт необходимых модулей.
from loguru import logger

from aiogram import Router
from aiogram.filters import ChatMemberUpdatedFilter, KICKED, IS_MEMBER
from aiogram.types import ChatMemberUpdated

from app.data_base.requests import MyRequests


# Инициализация роутера
router = Router(name=__name__)


# Обработчик блокировки бота пользователем.
@router.my_chat_member(ChatMemberUpdatedFilter(IS_MEMBER >> KICKED))
async def user_blocked_bot(event: ChatMemberUpdated) -> None:
    """Выводит в консоль соответствующее уведомление блокировки пользователем бота.
    Удаляет бота из базы данных (Из таблицы ВСЕХ пользователей). """

    user_id = event.from_user.id

    try:
        await MyRequests.delete_line('Users', 'user_id', user_id)

        logger.info(
            f'Пользователь {event.from_user.full_name} заблокировал бота!\n'
            f'ID: {user_id}\n\n'
        )
    except Exception as e:
        logger.error(f'An error has occurred {e}')
