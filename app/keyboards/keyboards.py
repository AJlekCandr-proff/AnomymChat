# -*- coding: utf-8 -*-


# Импорт необходимых модулей.
from aiogram.utils.keyboard import ReplyKeyboardBuilder, KeyboardButton, ReplyKeyboardMarkup


# Класс создания клавиатур.
class KeyBoard:
    """Класс для создания кнопок на клавиатуре. """

    def __init__(self, buttons: list[str]) -> None:
        """Метод создания класса.\n
        Принимает в себя список из строк для дальнейшего создания клавиатур. """

        self.buttons: list[str] = buttons

    def __call__(self, rows: int = None) -> ReplyKeyboardMarkup:
        """Возвращает объект класса ReplyKeyboardMarkup. """

        self.markup = ReplyKeyboardBuilder()

        for button in self.buttons:
            self.markup.add(KeyboardButton(text=button))

        self.markup = self.markup.adjust(rows).as_markup(resize_keyboard=True)

        return self.markup


# Создание объекта класса KeyBoard.
MainMenu = KeyBoard(
    [
        '🚀 Поиск случайного собеседника',
    ],
)


Cancel = KeyBoard(
    [
        'Стоп ❌',
    ],
)
