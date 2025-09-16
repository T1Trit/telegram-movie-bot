#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FilmsRew_bot - Телеграм бот для работы с фильмами и рецензиями
Автор: @FilmsRew_bot
Версия: 1.0
"""

import os
import random
from telebot import TeleBot, types

# Токен бота
BOT_TOKEN = os.environ.get('BOT_TOKEN', 'your_bot_token_here')
bot = TeleBot(BOT_TOKEN)

# База данных фильмов 2023 года
MOVIES_DB = {
    "action": [
        {"title": "Джон Уик 4", "rating": 8.0, "year": 2023, "director": "Чад Стахелски"},
        {"title": "Стражи Галактики 3", "rating": 8.1, "year": 2023, "director": "Джеймс Ганн"},
        {"title": "Форсаж 10", "rating": 5.8, "year": 2023, "director": "Луи Летерье"},
        {"title": "Индиана Джонс 5", "rating": 6.7, "year": 2023, "director": "Джеймс Мэнголд"},
    ],
    "drama": [
        {"title": "Оппенгеймер", "rating": 8.5, "year": 2023, "director": "Кристофер Нолан"},
        {"title": "Убийцы цветочной луны", "rating": 7.9, "year": 2023, "director": "Мартин Скорсезе"},
        {"title": "Зона интересов", "rating": 7.8, "year": 2023, "director": "Джонатан Глейзер"},
    ],
    "comedy": [
        {"title": "Барби", "rating": 7.0, "year": 2023, "director": "Грета Гервиг"},
        {"title": "Элементарно", "rating": 7.8, "year": 2023, "director": "Питер Сон"},
        {"title": "Подземелья и драконы", "rating": 7.3, "year": 2023, "director": "Джонатан Голдштейн"},
    ],
    "horror": [
        {"title": "Крик 6", "rating": 6.5, "year": 2023, "director": "Мэтт Беттинелли-Олпин"},
        {"title": "Зловещие мертвецы: Возрождение", "rating": 6.7, "year": 2023, "director": "Ли Кронин"},
        {"title": "Монахиня 2", "rating": 5.6, "year": 2023, "director": "Майкл Чавес"},
    ],
    "sci-fi": [
        {"title": "Дюна: Часть вторая", "rating": 8.7, "year": 2023, "director": "Дени Вильнёв"},
        {"title": "Человек-паук: Паутина вселенных", "rating": 8.6, "year": 2023, "director": "Хоакин Дос Сантос"},
    ]
}

# Состояния пользователей
user_states = {}

# Команды бота будут добавлены здесь
# Полный код доступен в репозитории