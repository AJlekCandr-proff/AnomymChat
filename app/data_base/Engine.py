# -*- coding: utf-8 -*-


# Импорт необходимых модулей.
from loguru import logger

from .Models import engine, Base


# Функция подключения к базе данных.
async def async_engine() -> None:
    """Подключает и обновляет базу данных"""

    async with engine.begin() as conn:
        try:
            await conn.run_sync(Base.metadata.create_all)

        except Exception as e:
            logger.error(f'An error has occurred {e}')
