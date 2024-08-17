# -*- coding: utf-8 -*-


__all__ = 'main_handlers_router'


# Импорт необходимых модулей.
from aiogram import Router

from .commands import router as main_commands_router
from .handler_open_chats import router as router_handler_dialogs
from .handler_events import router as router_handler_events
from .handler_anonym_chat import router as router_handler_chats


# Инициализация роутера.
router = Router(name=__name__)


# Подключение к главному роутеру других роутеров.
router.include_routers(
    main_commands_router,
    router_handler_dialogs,
    router_handler_events,
    router_handler_chats,
)
