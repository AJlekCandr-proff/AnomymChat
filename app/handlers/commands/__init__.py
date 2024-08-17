# -*- coding: utf-8 -*-


__all__ = 'main_commands_router'


# Импорт необходимых модулей.
from aiogram import Router

from .cmd_start import router as router_cmd_start


# Инициализация роутера.
router = Router()


# Подключение к главному роутеру команд других роутеров.
router.include_routers(
    router_cmd_start,

)
