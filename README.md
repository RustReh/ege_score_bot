Бот тренировочный Telegram.

Описание проекта
Бот тренировочный Telegram.
Бот создан для записи результатов экзаменов

Функции пользователя:
Возможность регистрироваться и записывать результаты своих экзаменов

Структура:

📦bot

┣ 📦database (пакет для работы базой данных)

┣ 📦filters (пакет для фильтров)

┣ 📦handlers (пакет эндпоинтов)

┣ 📦keyboards (пакет работы с клавиатурами бота)

┣ 📦middlewares (пакет с промежуточным по)

┣ 📦settings (пакет настроек)

┣ 📜main.py (модуль запуска телеграм бота)

┣ 📜requirements.txt 

┗ 📜env_template(файл для создания .env)

Запуск на локальном компьютере
Следуя этим инструкциям, вы получите копию проекта, которая будет запущена на вашем локальном компьютере для целей разработки и тестирования.

Инструкция по запуску
Клонировать копию проекта на локальный компьютер
В используемой вами IDE в корне проекта создаем виртуальную среду командой
python3.12 -m venv venv
И активируем ее
source venv/bin/activate
В корне проекта создаем файл переменных окружения .env с параметрами из template.env 

Для создания телеграм бота и получения токена воспользуйтесь инструкцией 

Устанавливаем зависимости
pip install -r requirements.txt
Запуск бота Телеграм
python main.py