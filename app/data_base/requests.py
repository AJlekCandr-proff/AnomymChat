# -*- coding: utf-8 -*-


# Импорт необходимых модулей.
from typing import Any

from sqlalchemy import (
    select, column, insert, update, delete
)

from .Models import *


# Класс для запросов к базе данных.
class Requests:
    """Класс для запросов к базе данных.\n
    Все методы преимущественно асинхронные. """

    # Метод создания класса.
    def __init__(self, *args: tuple[str, Any]) -> None:
        """Метод создания класса.\n
        Принимает в себя кортеж из названия и самого класса таблицы в базе данных. """

        self._session = async_session()
        self.__tables: dict = dict(args)

    async def get_columns(self, table: str, *columns_name: str) -> list[tuple]:
        """Возвращает список кортежей с данных указанных столбцов из указанной таблицы.\n
        Метод асинхронный. """

        async with self._session:
            table = self.__tables.get(table)

            query = select(*[column(name) for name in columns_name]).select_from(table)
            result = await self._session.execute(query)

            result = result.fetchall()

            return result

    async def get_line(self, table: str, column_name: str, value: Any) -> Any | None:
        """Возвращает строку с данным из указанной таблицы, данные возвращаются в виде ее же класса.\n
        Метод асинхронный. """

        async with self._session:
            table = self.__tables.get(table)

            query = select(table).where(column(column_name) == value)
            result = await self._session.execute(query)
            result = result.fetchone()

            if result is not None:
                return result[0]
            else:
                return None

    async def add_items(self, table: str, **kwargs: dict) -> None:
        """Добавляет данные в указанную таблицу.\n
        Метод асинхронный. """

        async with self._session:
            table = self.__tables.get(table)

            query = insert(table).values(kwargs).prefix_with('OR IGNORE')
            await self._session.execute(query)

            await self._session.commit()

    async def update_items(self, table: str, column_name: str, value: Any, **kwargs: dict) -> None:
        """Обновляет данные в указанном строке и в таблице.\n
        Метод асинхронный. """

        async with self._session:
            table = self.__tables.get(table)

            query = update(table).where(column(column_name) == value).values(kwargs)
            await self._session.execute(query)

            await self._session.commit()

    async def delete_line(self, table: str, column_name: str, value: Any) -> None:
        """Удаляет строку в указанной таблице
        с указанными параметром в определенном столбце.\n
        Метод асинхронный. """

        async with self._session:
            table = self.__tables.get(table)

            query = delete(table).where(column(column_name) == value)
            await self._session.execute(query)

            await self._session.commit()


# Создание объекта класса Requests.
MyRequests = Requests(
    *[
        ('SearchUsers', SearchUsers),
        ('Users', Users),
        ('Dialogs', Dialogs),
    ],
)
