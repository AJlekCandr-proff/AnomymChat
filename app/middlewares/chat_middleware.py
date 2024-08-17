# -*- coding: utf-8 -*-


# Импорт необходимых модулей.
from loguru import logger

from typing import Any, Callable, Awaitable, Dict

from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import Message

from app.data_base.requests import MyRequests


# Класс middleware для чатов.
class ChatMiddleware(BaseMiddleware):
    """Класс middleware. \n
    Проверяет то, находится ли пользователь в диалоге с кем-то.
    Если это так, то сообщение обрабатывается основным обработчиком. """

    async def __call__(
            self,
            handler: Callable[
                [
                    Message,
                    Dict[Any, str],
                ],
                Awaitable[Any],
            ],
            event: Message,
            data: Dict[Any, str | Dict[str, Any]],
    ) -> Any:
        try:
            user_id = event.from_user.id
            dialog = await MyRequests.get_line('Dialogs', 'user_1', user_id) or await MyRequests.get_line('Dialogs', 'user_2', user_id)

            if dialog:
                companion = dialog.user_1 ^ dialog.user_2 ^ user_id
                data['info'] = {'user': dialog.user_1, 'companion': companion, 'messages': dialog.messages}

                return await handler(event, data)

        except Exception as e:
            logger.error(f'An error has occurred {e}')
