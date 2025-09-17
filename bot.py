#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os
import random
import json
import re
from datetime import datetime
from typing import List, Dict, Any

import telebot
from telebot import types

BOT_TOKEN = os.environ.get('BOT_TOKEN', '7595500623:AAFMBKBvRi2eA0PRb2QHE1_tB6V_cnx3fHw')
bot = telebot.TeleBot(BOT_TOKEN)

# База данных фильмов 2023 года с рейтингами и жанрами
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

# Состояния пользователей для отслеживания контекста
user_states = {}

# Цитаты из фильмов
MOVIE_QUOTES = [
    "«Я сделаю ему предложение, от которого он не сможет отказаться» — Крёстный отец",
    "«Да пребудет с тобой Сила» — Звёздные войны",
    "«Жизнь как коробка шоколадных конфет» — Форрест Гамп",
    "«Хьюстон, у нас проблема» — Аполлон 13",
    "«Я вернусь» — Терминатор",
    "«После всего, я думаю, мы не в Канзасе» — Волшебник страны Оз",
    "«Элементарно, Ватсон» — Шерлок Холмс",
]

# Факты о кино
MOVIE_FACTS = [
    "🎬 Самый длинный фильм в истории длится 857 часов (35 дней)!",
    "🏆 'Оппенгеймер' получил 7 Оскаров в 2024 году",
    "💰 'Аватар: Путь воды' собрал более 2.3 миллиарда долларов",
    "📽️ Первый фильм был снят в 1888 году и длился всего 2 секунды",
    "🎭 Том Круз выполняет все трюки в 'Миссия невыполнима' самостоятельно",
    "🦖 Для 'Парка Юрского периода' звуки динозавров создавали из криков животных",
    "🌍 Болливуд производит больше фильмов в год, чем Голливуд",
]


@bot.message_handler(commands=['start'])
def send_welcome(message):
    """Обработчик команды /start - приветствие и объяснение функционала"""
    user_id = message.from_user.id
    user_name = message.from_user.first_name or "Киноман"
    
    # Создаем красивое приветственное сообщение
    welcome_text = f"""
🎬 *Добро пожаловать в FilmsRew Bot, {user_name}!*

Я — ваш персональный помощник в мире кино 2023 года!

🎯 *Что я умею:*

📌 /help - Показать все доступные команды
🎲 /random\_movie - Получить случайную рекомендацию фильма
🔍 /find\_movie \[жанр\] - Найти фильм по жанру
⭐ /top\_rated - Топ-5 фильмов по рейтингу
💬 /movie\_quote - Случайная цитата из фильма
📚 /movie\_fact - Интересный факт о кино
🎮 /quiz - Викторина о фильмах

💡 *Примеры использования:*
• /find\_movie action - найти боевик
• /find\_movie drama - найти драму
• /random\_movie - случайный фильм

Готовы погрузиться в мир кино? 🍿
    """
    
    # Создаем клавиатуру с быстрыми командами
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton("🎲 Случайный фильм")
    btn2 = types.KeyboardButton("⭐ Топ фильмов")
    btn3 = types.KeyboardButton("💬 Цитата")
    btn4 = types.KeyboardButton("📚 Факт о кино")
    markup.add(btn1, btn2, btn3, btn4)
    
    bot.send_message(message.chat.id, welcome_text, parse_mode='Markdown', reply_markup=markup)


@bot.message_handler(commands=['help'])
def send_help(message):
    """Обработчик команды /help - список всех команд"""
    help_text = """
📋 *Доступные команды:*

*Основные команды:*
🏠 /start - Начать работу с ботом
❓ /help - Показать это сообщение

*Работа с фильмами:*
🎲 /random\_movie - Случайная рекомендация фильма
🔍 /find\_movie \[жанр\] - Найти фильм по жанру
⭐ /top\_rated - Топ-5 фильмов 2023 года

*Развлечения:*
💬 /movie\_quote - Случайная цитата из фильма
📚 /movie\_fact - Интересный факт о кино
🎮 /quiz - Мини-викторина о фильмах

*Доступные жанры:*
• action (боевик)
• drama (драма)
• comedy (комедия)
• horror (ужасы)
• sci-fi (фантастика)

*Примеры:*
/find\_movie comedy - найти комедию
/find\_movie action - найти боевик
    """
    
    bot.send_message(message.chat.id, help_text, parse_mode='Markdown')


@bot.message_handler(commands=['random_movie'])
def random_movie(message):
    """Команда для получения случайной рекомендации фильма"""
    # Выбираем случайный жанр
    genre = random.choice(list(MOVIES_DB.keys()))
    # Выбираем случайный фильм из этого жанра
    movie = random.choice(MOVIES_DB[genre])
    
    # Генерируем рекомендацию с эмодзи в зависимости от рейтинга
    if movie['rating'] >= 8.0:
        emoji = "🔥"
        recommendation = "Обязательно к просмотру!"
    elif movie['rating'] >= 7.0:
        emoji = "👍"
        recommendation = "Отличный выбор для вечера!"
    else:
        emoji = "🎬"
        recommendation = "Неплохой фильм для разнообразия"
    
    response = f"""
{emoji} *Случайная рекомендация:*

🎬 *{movie['title']}* ({movie['year']})
🎭 Жанр: {genre}
👤 Режиссёр: {movie['director']}
⭐ Рейтинг: {movie['rating']}/10

💡 {recommendation}
    """
    
    # Добавляем инлайн-кнопку для новой рекомендации
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("🎲 Ещё фильм", callback_data="random_movie")
    markup.add(btn)
    
    bot.send_message(message.chat.id, response, parse_mode='Markdown', reply_markup=markup)


@bot.message_handler(commands=['find_movie'])
def find_movie(message):
    """Команда для поиска фильма по жанру с обработкой аргументов"""
    # Парсим аргументы команды
    args = message.text.split()[1:] if len(message.text.split()) > 1 else []
    
    if not args:
        # Если жанр не указан, показываем клавиатуру с выбором
        markup = types.InlineKeyboardMarkup()
        for genre in MOVIES_DB.keys():
            btn = types.InlineKeyboardButton(
                f"🎬 {genre.capitalize()}", 
                callback_data=f"genre_{genre}"
            )
            markup.add(btn)
        
        bot.send_message(
            message.chat.id, 
            "Выберите жанр фильма:", 
            reply_markup=markup
        )
        return
    
    # Обрабатываем указанный жанр
    genre = args[0].lower()
    
    # Проверяем наличие жанра в базе
    if genre not in MOVIES_DB:
        available = ", ".join(MOVIES_DB.keys())
        bot.send_message(
            message.chat.id,
            f"❌ Жанр '{genre}' не найден.\n\n"
            f"Доступные жанры: {available}"
        )
        return
    
    # Выбираем фильмы указанного жанра
    movies = MOVIES_DB[genre]
    
    # Сортируем по рейтингу и берем лучшие
    top_movies = sorted(movies, key=lambda x: x['rating'], reverse=True)[:3]
    
    response = f"🎬 *Лучшие фильмы в жанре {genre}:*\n\n"
    
    for i, movie in enumerate(top_movies, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉"
        response += f"{medal} *{movie['title']}*\n"
        response += f"   ⭐ Рейтинг: {movie['rating']}/10\n"
        response += f"   👤 Режиссёр: {movie['director']}\n\n"
    
    bot.send_message(message.chat.id, response, parse_mode='Markdown')


@bot.message_handler(commands=['top_rated'])
def top_rated(message):
    """Команда для показа топ-5 фильмов по рейтингу"""
    # Собираем все фильмы в один список
    all_movies = []
    for genre, movies in MOVIES_DB.items():
        for movie in movies:
            movie_with_genre = movie.copy()
            movie_with_genre['genre'] = genre
            all_movies.append(movie_with_genre)
    
    # Сортируем по рейтингу
    top_movies = sorted(all_movies, key=lambda x: x['rating'], reverse=True)[:5]
    
    response = "🏆 *ТОП-5 фильмов 2023 года:*\n\n"
    
    medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣"]
    
    for i, movie in enumerate(top_movies):
        response += f"{medals[i]} *{movie['title']}*\n"
        response += f"   ⭐ Рейтинг: {movie['rating']}/10\n"
        response += f"   🎭 Жанр: {movie['genre']}\n"
        response += f"   👤 Режиссёр: {movie['director']}\n\n"
    
    # Добавляем статистику
    avg_rating = sum(m['rating'] for m in top_movies) / len(top_movies)
    response += f"📊 Средний рейтинг топ-5: {avg_rating:.1f}/10"
    
    bot.send_message(message.chat.id, response, parse_mode='Markdown')


@bot.message_handler(commands=['movie_quote'])
def movie_quote(message):
    """Команда для получения случайной цитаты из фильма"""
    quote = random.choice(MOVIE_QUOTES)
    
    response = f"💬 *Цитата дня:*\n\n_{quote}_"
    
    # Добавляем кнопку для новой цитаты
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("💬 Ещё цитата", callback_data="quote")
    markup.add(btn)
    
    bot.send_message(message.chat.id, response, parse_mode='Markdown', reply_markup=markup)


@bot.message_handler(commands=['movie_fact'])
def movie_fact(message):
    """Команда для получения интересного факта о кино"""
    fact = random.choice(MOVIE_FACTS)
    
    response = f"📚 *Интересный факт:*\n\n{fact}"
    
    # Добавляем кнопку для нового факта
    markup = types.InlineKeyboardMarkup()
    btn = types.InlineKeyboardButton("📚 Ещё факт", callback_data="fact")
    markup.add(btn)
    
    bot.send_message(message.chat.id, response, parse_mode='Markdown', reply_markup=markup)


@bot.message_handler(commands=['quiz'])
def start_quiz(message):
    """Команда для запуска викторины о фильмах"""
    user_id = message.from_user.id
    
    # Подготавливаем вопрос викторины
    questions = [
        {
            "question": "Какой фильм получил Оскар за лучший фильм в 2024 году?",
            "options": ["Оппенгеймер", "Барби", "Убийцы цветочной луны", "Зона интересов"],
            "correct": 0
        },
        {
            "question": "Кто режиссёр фильма 'Дюна: Часть вторая'?",
            "options": ["Кристофер Нолан", "Дени Вильнёв", "Мартин Скорсезе", "Джеймс Кэмерон"],
            "correct": 1
        },
        {
            "question": "Какой фильм собрал больше всего в прокате в 2023?",
            "options": ["Барби", "Оппенгеймер", "Стражи Галактики 3", "Форсаж 10"],
            "correct": 0
        },
        {
            "question": "Сколько частей в серии фильмов о Джоне Уике?",
            "options": ["3", "4", "5", "6"],
            "correct": 1
        },
        {
            "question": "Какой актёр играет главную роль в 'Оппенгеймере'?",
            "options": ["Роберт Дауни мл.", "Киллиан Мёрфи", "Мэтт Деймон", "Том Харди"],
            "correct": 1
        }
    ]
    
    # Выбираем случайный вопрос
    quiz = random.choice(questions)
    
    # Сохраняем правильный ответ для пользователя
    user_states[user_id] = {"quiz_answer": quiz["correct"]}
    
    # Создаем клавиатуру с вариантами ответов
    markup = types.InlineKeyboardMarkup(row_width=2)
    for i, option in enumerate(quiz["options"]):
        btn = types.InlineKeyboardButton(option, callback_data=f"quiz_{i}")
        markup.add(btn)
    
    response = f"🎮 *Викторина о кино*\n\n❓ {quiz['question']}"
    
    bot.send_message(message.chat.id, response, parse_mode='Markdown', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    """Обработчик всех callback-запросов от инлайн-кнопок"""
    user_id = call.from_user.id
    
    if call.data == "random_movie":
        # Генерируем новый случайный фильм
        genre = random.choice(list(MOVIES_DB.keys()))
        movie = random.choice(MOVIES_DB[genre])
        
        if movie['rating'] >= 8.0:
            emoji = "🔥"
            recommendation = "Обязательно к просмотру!"
        elif movie['rating'] >= 7.0:
            emoji = "👍"
            recommendation = "Отличный выбор для вечера!"
        else:
            emoji = "🎬"
            recommendation = "Неплохой фильм для разнообразия"
        
        response = f"""
{emoji} *Случайная рекомендация:*

🎬 *{movie['title']}* ({movie['year']})
🎭 Жанр: {genre}
👤 Режиссёр: {movie['director']}
⭐ Рейтинг: {movie['rating']}/10

💡 {recommendation}
        """
        
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("🎲 Ещё фильм", callback_data="random_movie")
        markup.add(btn)
        
        bot.edit_message_text(
            response, 
            call.message.chat.id, 
            call.message.message_id,
            parse_mode='Markdown',
            reply_markup=markup
        )
        
    elif call.data.startswith("genre_"):
        # Обработка выбора жанра
        genre = call.data.replace("genre_", "")
        movies = MOVIES_DB[genre]
        top_movies = sorted(movies, key=lambda x: x['rating'], reverse=True)[:3]
        
        response = f"🎬 *Лучшие фильмы в жанре {genre}:*\n\n"
        
        for i, movie in enumerate(top_movies, 1):
            medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉"
            response += f"{medal} *{movie['title']}*\n"
            response += f"   ⭐ Рейтинг: {movie['rating']}/10\n"
            response += f"   👤 Режиссёр: {movie['director']}\n\n"
        
        bot.edit_message_text(
            response,
            call.message.chat.id,
            call.message.message_id,
            parse_mode='Markdown'
        )
        
    elif call.data == "quote":
        # Новая цитата
        quote = random.choice(MOVIE_QUOTES)
        response = f"💬 *Цитата дня:*\n\n_{quote}_"
        
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("💬 Ещё цитата", callback_data="quote")
        markup.add(btn)
        
        bot.edit_message_text(
            response,
            call.message.chat.id,
            call.message.message_id,
            parse_mode='Markdown',
            reply_markup=markup
        )
        
    elif call.data == "fact":
        # Новый факт
        fact = random.choice(MOVIE_FACTS)
        response = f"📚 *Интересный факт:*\n\n{fact}"
        
        markup = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("📚 Ещё факт", callback_data="fact")
        markup.add(btn)
        
        bot.edit_message_text(
            response,
            call.message.chat.id,
            call.message.message_id,
            parse_mode='Markdown',
            reply_markup=markup
        )
        
    elif call.data.startswith("quiz_"):
        # Обработка ответа на викторину
        answer_index = int(call.data.replace("quiz_", ""))
        
        if user_id in user_states and "quiz_answer" in user_states[user_id]:
            correct_answer = user_states[user_id]["quiz_answer"]
            
            if answer_index == correct_answer:
                response = "✅ *Правильно!* Отличные знания кино! 🎬"
            else:
                response = "❌ *Неправильно!* Попробуйте ещё раз с новым вопросом 🎮"
            
            # Убираем состояние
            del user_states[user_id]
            
            # Добавляем кнопку для нового вопроса
            markup = types.InlineKeyboardMarkup()
            btn = types.InlineKeyboardButton("🎮 Новый вопрос", callback_data="new_quiz")
            markup.add(btn)
            
            bot.edit_message_text(
                response,
                call.message.chat.id,
                call.message.message_id,
                parse_mode='Markdown',
                reply_markup=markup
            )
            
    elif call.data == "new_quiz":
        # Новый вопрос викторины
        questions = [
            {
                "question": "В каком году вышел первый фильм о Гарри Поттере?",
                "options": ["1999", "2000", "2001", "2002"],
                "correct": 2
            },
            {
                "question": "Какой фильм первым преодолел отметку в 1 миллиард долларов?",
                "options": ["Титаник", "Аватар", "Звёздные войны", "Парк Юрского периода"],
                "correct": 0
            },
            {
                "question": "Сколько фильмов в основной саге 'Звёздных войн'?",
                "options": ["6", "7", "8", "9"],
                "correct": 3
            }
        ]
        
        quiz = random.choice(questions)
        user_states[user_id] = {"quiz_answer": quiz["correct"]}
        
        markup = types.InlineKeyboardMarkup(row_width=2)
        for i, option in enumerate(quiz["options"]):
            btn = types.InlineKeyboardButton(option, callback_data=f"quiz_{i}")
            markup.add(btn)
        
        response = f"🎮 *Викторина о кино*\n\n❓ {quiz['question']}"
        
        bot.edit_message_text(
            response,
            call.message.chat.id,
            call.message.message_id,
            parse_mode='Markdown',
            reply_markup=markup
        )
    
    # Отвечаем на callback, чтобы убрать "часики"
    bot.answer_callback_query(call.id)


@bot.message_handler(func=lambda message: True)
def handle_text(message):
    """Обработчик текстовых сообщений (кнопки быстрого доступа)"""
    text = message.text
    
    if text == "🎲 Случайный фильм":
        random_movie(message)
    elif text == "⭐ Топ фильмов":
        top_rated(message)
    elif text == "💬 Цитата":
        movie_quote(message)
    elif text == "📚 Факт о кино":
        movie_fact(message)
    else:
        # Обработка произвольного текста - поиск фильма
        search_text = text.lower()
        found_movies = []
        
        # Ищем фильмы по названию
        for genre, movies in MOVIES_DB.items():
            for movie in movies:
                if search_text in movie['title'].lower():
                    movie_with_genre = movie.copy()
                    movie_with_genre['genre'] = genre
                    found_movies.append(movie_with_genre)
        
        if found_movies:
            response = f"🔍 *Найдено фильмов: {len(found_movies)}*\n\n"
            for movie in found_movies[:3]:  # Показываем максимум 3
                response += f"🎬 *{movie['title']}*\n"
                response += f"   🎭 Жанр: {movie['genre']}\n"
                response += f"   ⭐ Рейтинг: {movie['rating']}/10\n\n"
        else:
            response = (
                "🤔 Не могу найти такой фильм.\n\n"
                "Попробуйте использовать команды:\n"
                "/random_movie - случайный фильм\n"
                "/find_movie [жанр] - поиск по жанру\n"
                "/help - все команды"
            )
        
        bot.send_message(message.chat.id, response, parse_mode='Markdown')


def main():
    """Главная функция запуска бота"""
    print("🎬 FilmsRew Bot запущен!")
    print(f"🔗 Бот доступен: https://t.me/FilmsRew_bot")
    print("⏳ Ожидание сообщений...")
    
    # Запускаем бота с обработкой ошибок
    while True:
        try:
            bot.polling(none_stop=True, interval=0)
        except Exception as e:
            print(f"❌ Ошибка: {e}")
            print("🔄 Перезапуск через 5 секунд...")
            import time
            time.sleep(5)


if __name__ == '__main__':
    main()
