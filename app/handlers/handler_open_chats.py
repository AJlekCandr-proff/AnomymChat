# -*- coding: utf-8 -*-


# Импорт необходимых модулей.
from loguru import logger

import asyncio

import random

from aiogram import Router, F
from aiogram.types import Message

from app.data_base.requests import MyRequests
from app.bot_settings import bot
from app.keyboards.keyboards import *


# Инициализация роутера.
router = Router(name=__name__)


# Функция создания диалога.
async def choice_companions(message: Message, user_id: int) -> None:
    """В качестве аргументов принимает в себя объект класса
    Message и ID пользователя.\n
    Из базы данных берет список пользователей, которые так же
    открыли поиск собеседника и начинает цикл поиска.
      Если в списке больше чем 1 пользователь, то с помощью модуля
    random выбирается случайный пользователь. При этом, если выбранный собеседник не сам пользователь,
    то оба собеседника добавляются в базу данных и начинается диалог (Диалогу присваивается уникальный ID)
    и цикл завершается. В противном случае, пишется предупредительное сообщение и цикл продолжается.\n
    Функция асинхронная. """

    dialog_companions = [user_id]
    users_id = await MyRequests.get_columns('SearchUsers', 'user_id')
    users_id = [user_id[0] for user_id in users_id]

    logger.info(f'Все пользователи, находящиеся в поиске собеседника: {users_id}')

    while len(users_id) > 0:
        if len(users_id) > 1:
            companion = random.choice(users_id)

            if companion != user_id:
                dialog_companions.append(companion)

                await MyRequests.add_items('Dialogs', user_1=user_id, user_2=companion)

                for companion in dialog_companions:
                    await MyRequests.delete_line('SearchUsers', 'user_id', companion)

                    await bot.send_message(
                        chat_id=companion,
                        text='Собеседник найден!\n\n',
                        reply_markup=Cancel(1),
                    )
                logger.info(f'Начался диалог между пользователями {user_id}')

                break

            else:
                logger.info(f'По случайности с пользователем {user_id} случилась ошибка в поиске!')
        else:
            await asyncio.sleep(5)

            await message.answer(
                text='🕓 Поиск собеседника слишком долгий, это может занять больше времени, чем обычно...\n\n',
            )

            logger.info(
                f'В состоянии поиска недостаточно пользователей, '
                f'повторный поиск для пользователя {user_id} собеседника...'
            )


# Обработчик кнопки '🚀 Поиск случайного собеседника'.
@router.message(F.text == '🚀 Поиск случайного собеседника')
async def search_companion(message: Message) -> None:
    """Записывает пользователя в базу данных. \n
    Открывает поиск собеседника и начинает диалог. """

    user_id = message.from_user.id
    button_text = message.text

    try:
        user = await MyRequests.get_line('Users', 'user_id', user_id)

        await MyRequests.add_items('SearchUsers', user_id=user_id, full_name=user.full_name)

        if button_text == '🚀 Поиск случайного собеседника':
            await message.answer(
                text='🔎 Поиск собеседника... \n\n',
            )
            logger.info(f'Пользователь {user_id} открыл поиск собеседника в анонимном чате!')

            await choice_companions(message, user_id)

    except Exception as e:
        logger.error(f'An error has occurred {e}')
