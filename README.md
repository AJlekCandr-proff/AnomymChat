# AnomymChat
## Проект Вязникова Александра. Анонимный чат в Telegram-боте. Работа с Telegram Bot API.
## Документация проекта "Анонимный чат". О проделанной работе, структуре.

##Введение
Проект "Анонимный чат" представляет собой Telegram-бота, который позволяет пользователям общаться один на один с случайными собеседниками. Этот бот обеспечивает анонимность, простоту использования и соблюдение правил общения. В данной документации подробно описаны ключевые функции, архитектура проекта, используемые технологии и подходы к разработке.
###Основные функции бота
###1. Запуск бота
Для начала работы с ботом пользователь должен ввести команду /start.
Обработчик: cmd_start.py
Функция: cmd_start
####Описание:
При получении команды бот отправляет приветственное сообщение, которое включает правила общения:
текст
👋 Привет! Это Анонимный чат Telegram.
Тут можно общаться 1 на 1 со случайными собеседниками 💬
📖 В чате есть правила поведения, которые нужно соблюдать.
Нельзя спамить, продвигать свои услуги, оскорблять собеседников.
Удачного общения! Будьте вежливы к собеседникам ❤️
скорее начинай общение 👇🏻

Параллельно с сообщением пользователю отображается клавиатура с кнопкой "🚀 Поиск случайного собеседника".
Пользователь добавляется в базу данных в таблицу "Users", если его там еще нет.
###2. Поиск собеседника
Когда пользователь нажимает кнопку "🚀 Поиск случайного собеседника", запускается процесс поиска.
Обработчик: handler_open_chats.py
Функция: search_companion
####Описание:
Бот извлекает данные из таблицы "Users" и записывает информацию в таблицу "SearchUsers", где хранятся пользователи, которые также ищут собеседника.
Пользователь получает сообщение "🔎 Поиск собеседника...", уведомляющее о начале процесса поиска.
###3. Выбор собеседника
После того как пользователь начал поиск, бот выбирает случайного собеседника.
Функция: choice_companions
####Описание:
Функция принимает объект класса Message и ID пользователя.
Из таблицы "SearchUsers" извлекается список пользователей, которые также ищут собеседника.
Если в списке больше одного пользователя, с помощью модуля random выбирается случайный собеседник.
Если выбранный собеседник не совпадает с текущим пользователем, оба добавляются в таблицу "Dialogs", и начинается диалог.
В противном случае выводится сообщение о том, что выбранный собеседник не может быть самим пользователем, и поиск продолжается.
###4. Обработка сообщений
Для управления сообщениями пользователей используется middleware.
Промежуточное программное обеспечение: chat_middleware.py
####Описание:
Этот класс обрабатывает события перед основным обработчиком.
Он проверяет, находится ли пользователь в диалоге, проверяя таблицу "Dialogs".
Если пользователь ведет диалог, его сообщения пересылаются собеседнику, а база данных обновляется с учетом количества отправленных сообщений.
###5. Завершение диалога
Пользователи могут завершить диалог в любой момент.
Обработчик: stop_dialog
####Описание:
При нажатии кнопки "Стоп ❌" срабатывает обработчик, который завершает диалог.
Диалог автоматически удаляется из базы данных, а пользователи получают уведомление о завершении:
текст
❗️Диалог завершен
Вы отправили <кол-во сообщений, отправленных во время диалога> сообщений! 💬

После завершения диалога пользователи возвращаются в главное меню с возможностью снова найти собеседника.
###6. Обработка блокировок
Бот также обрабатывает случаи, когда пользователь блокирует его.
Обработчик: user_blocked_bot
####Описание:
При блокировке бота пользователем срабатывает асинхронная функция, которая удаляет пользователя из базы данных "Users".
Архитектура проекта
###Проект организован по следующей структуре:
текст
app/
├── handlers/
│   ├── commands/
│   │   └── cmd_start.py
│   ├── handler_anonym_chat.py
│   ├── handler_events.py
│   └── handler_open_chats.py
├── middlewares/
│   └── chat_middleware.py
├── keyboards/
│   └── keyboards.py
├── data_base/
│   ├── data_base.db
│   ├── Models.py
│   ├── requests.py
│   └── Engine.py
├── bot_settings.py
└── requirements.txt

###Используемые технологии
Python: Основной язык программирования, на котором реализован проект.
AIOgram: Библиотека для работы с Telegram Bot API, обеспечивающая асинхронную обработку сообщений.
AIOhttp: Используется для выполнения асинхронных HTTP-запросов.
Asyncio: Модуль для работы с асинхронным программированием, позволяющий эффективно управлять задачами.
SQLAlchemy: ORM для работы с базами данных, упрощающая взаимодействие с SQL.
AIOSQLite: Асинхронная библиотека для работы с SQLite, позволяющая выполнять запросы без блокировки основного потока.
pydantic_settings: Библиотека для работы с переменными окружения, обеспечивающая безопасность и удобство доступа к ним.
Логирование и обработка ошибок
В проекте реализовано логирование с использованием конструкции try-finally для отслеживания ошибок и отладки работы программы. Это позволяет выявлять и устранять проблемы в реальном времени.

В файле requirements.txt указаны все необходимые зависимости для корректной работы программы.

В ходе создания программы я использовал свои навыки и знания языка Python и работы с его сторонними библиотеками и объекта-ориентированным программированием в целом, работой с асинхронностью, логированием процессов и обработкой тех или иных ошибок, подключение и грамотная работа с Telegram Bot API, работа с перменными окружения с помощью, уже ранее упомянутой библиотеки, pydantic_settings.Проявил навыки работы с мощной базой данных SQLalchemy и AIOSQLite: Создание асинронных запросов к БД.
