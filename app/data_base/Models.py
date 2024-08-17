# -*- coding: utf-8 -*-


# Импорт необходимых модулей.
from app.bot_settings import settings

from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import BigInteger, Text


# Инициализация сессии.
engine = create_async_engine(settings.SQLALCHEMY_URL)


# Инициализация сессии.
async_session = async_sessionmaker(engine)


# Класс базы данных.
class Base(DeclarativeBase):
    """Класс базы данных. """

    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


# Класс общих параметров таблиц пользователей.
class UsersItems(Base):
    """Абстрактный класс.\n
    Хранит в себе общие столбцы-параметры таблиц базы данных. """

    __abstract__ = True

    user_id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
    full_name: Mapped[str] = mapped_column(Text, nullable=False, unique=True)


# Класс таблицы ВСЕХ пользователей бота, которые не блокировали бота.
class Users(UsersItems):
    """Класс таблицы в базе данных.\n
    Хранит информацию о ВСЕХ пользователях,
    которые пользуются ботом и не блокировали бота. """

    __tablename__ = 'Users'


# Класс таблицы пользователей, которые в поиске собеседника.
class SearchUsers(UsersItems):
    """Класс таблицы в базе данных.\n
    Хранит информацию о пользователях, которые открыли поиск собеседника. """

    __tablename__ = 'SearchUsers'


# Класс таблицы диалогов.
class Dialogs(Base):
    """Класс таблицы в базе данных.\n
    Хранит в себе основную информацию о ведущихся диалогах. """

    __tablename__ = 'Dialogs'

    user_1: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
    user_2: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True)
    messages: Mapped[int] = mapped_column(BigInteger, nullable=False, default=0)
