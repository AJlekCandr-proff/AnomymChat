# -*- coding: utf-8 -*-


# Необходимых модулей.
from pydantic_settings import BaseSettings

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties


# Класс настроек бота.
class Settings(BaseSettings):
    """Хранит в себе переменные окружения проекта. """

    TOKEN: str
    SQLALCHEMY_URL: str

    class Config:
        """Конфигурация. """

        env_file: str = '.env'


# Создание объекта класса Settings.
settings = Settings()


# Инициализация бота.
bot = Bot(
    token=settings.TOKEN,
    default=DefaultBotProperties(
        parse_mode='HTML',
    ),
)
