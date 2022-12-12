"""
This file is a part of AnimeGo Monitoring Bot.

AnimeGo Monitoring Bot is a Telegram bot supposed to check the release of new episodes at <https://animego.org/>
Copyright (C) 2021 Nerovik

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import requests
import threading
from time import sleep
import agparser as parser
from datetime import datetime

from database import Database
db = Database("tracking.db") # Подключение к базе данных

bot = telebot.TeleBot("<API-ключ>", "HTML") # Вставляем сюда свой API-ключ

# Функция, которая один раз в какое-то кол-во времени проверяет вышла ли новая серия
def checker_test():
    while True:
        time = datetime.now()
        timestamp = f'[{time.day}-{time.month}-{time.year} {time.hour}:{time.minute}:{time.second}]'

        for tuple in db.getIds(): # Получаем все кортежи из списка в БД
            for id in tuple: # Из каждого кортежа извлекаем значение и производим операции
                userId = db.getUserId(id)
                link = db.getTracking(id)

                thumbnail = parser.getThumbnail(link)
                episodes = parser.getEpisodes(link) # Получаем с ресурса количество эпизодов на тайтле пользователя
                title = parser.getTitle(link) 
                status = parser.getStatus(link)
                studio = parser.getStudio(link)

                if (episodes != db.getEpisodes(id)): # Сравниваем со значением в базе и если оно изменилось - отправляем сообщение
                    bot.send_photo(userId, requests.get(thumbnail).content, f'<b>{title}</b> \n'
                    '========================\n'
                    f'Эпизодов: {episodes}\n'
                    f'Статус: {status}\n'
                    f'Студия: {studio}\n'
                    '========================\n'
                    '<b>✅ Вышел новый эпизод этого аниме!</b>\n'
                    f'<b>Бегом смотреть: </b><a href="{db.getTracking(id)}">*тык*</a>')

                    db.setEpisodes(id, episodes)
                    print(f'{timestamp} Произошла проверка, уведомления о новых сериях отправлены')
                else:
                    print(f'{timestamp} Произошла проверка, новых серий нет')
        sleep(120) # Можно настроить любое время, в моём случае - это одна минута


# Делаем из функции поток и запускаем его
t1 = threading.Thread(target=checker_test) 
lock = threading.RLock()
t1.start()


# Хендлер, который отвечает за все команды, и да меня не колышет, что это так работать не должно
@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == "/start":
        userExists(message.from_user.id)

        bot.send_message(message.from_user.id, "👋 Привет, я бот для отслеживания выхода новых эпизодов разных аниме\n"
        "Напишите /help для просмотра списка команд, если вы тут впервые!\n\n"
        "✉️ Если появились вопросы или проблемы свяжитесь с разработчицей: <a href='https://notabug.org/ICQ/information/src/master/contacting_ru.txt'>*тык*</a>\n\n"
        "💰 Ссылка на пожертвования: <a href='https://notabug.org/ICQ/information/src/master/donations_ru.txt'>*тык*</a>\n\n"
        "⚙️ Ссылка на исходный код бота: <a href='https://notabug.org/ICQ/animego-monitoring_bot'>*тык*</a>")
    if message.text == "/help":
        bot.send_message(message.from_user.id, "/help - вывести список команд\n"
        "/tracking - вывести отслеживаемый тайтл\n"
        "/track - добавить тайтл в отслеживаемое")
    if message.text == "/tracking":
        userExists(message.from_user.id)

        if db.getTracking(db.getId(message.from_user.id)) == None:
            bot.send_message(message.from_user.id, "⛔️ Вы ничего не отслеживаете в данный момент!")
        else:
            link = db.getTracking(db.getId(message.from_user.id))
            episodes = db.getEpisodes(db.getId(message.from_user.id))

            title = parser.getTitle(link) 
            status = parser.getStatus(link)
            studio = parser.getStudio(link)

            bot.send_photo(message.from_user.id, requests.get(parser.getThumbnail(db.getTracking(db.getId(message.from_user.id)))).content, f'<b>{title}</b> \n'
            '========================\n'
            f'Эпизодов: {episodes}\n'
            f'Статус: {status}\n'
            f'Студия: {studio}\n'
            '========================\n'
            '<b>🔥 Вы отслеживаете это аниме!</b>') 
    if message.text == "/track":
        userExists(message.from_user.id)

        bot.send_message(message.from_user.id, "🔍 Какое аниме вы хотите отслеживать?")
        bot.register_next_step_handler(message, monitor) # Передаём задачу по добавлению тайтла другой функции
    if message.text == "/stoptracking":
        userExists(message.from_user.id)

        if db.getTracking(db.getId(message.from_user.id)) == None:
            bot.send_message(message.from_user.id, "⛔️ Вы ничего не отслеживаете в данный момент!")
        else:
            # Стираем записи пользователя.
            db.setTracking(db.getId(message.from_user.id), None) 
            db.setEpisodes(db.getId(message.from_user.id), None)
            bot.send_message(message.from_user.id, "🚫 Вы больше ничего не отслеживаете!")

# Функция, которая добавляет тайтл в отслеживаемые
def monitor(message):
    if parser.search(message.text) == None:
        bot.send_message(message.from_user.id, "❌ Мы не смогли найти аниме с таким названием. Убедитесь, что вы написали название правильно!")
    else:
        link = parser.search(message.text) # Парсим ссылку на тайтл
        markup = InlineKeyboardMarkup()
        go_button = InlineKeyboardButton(text='Перейти на страницу', url=link) # Создаём снизу сообщения кнопку
        markup.add(go_button)

        # Парсим всё! Обложку, название, количество эпизодов, студию, статус, только жанры пока не научился
        thumbnail = parser.getThumbnail(link)
        episodes = parser.getEpisodes(link) # Получаем с ресурса количество эпизодов на тайтле пользователя
        title = parser.getTitle(link) 
        status = parser.getStatus(link)
        studio = parser.getStudio(link)

        # Пользователь не сможет добавить уже вышедшее или ещё только анонсированное аниме
        if parser.getStatus(link) == 'Онгоинг' or parser.getStatus(link) == 'Анонс':
            bot.send_photo(message.from_user.id, requests.get(thumbnail).content, f'<b>{title}</b> \n'
            '========================\n'
            f'Эпизодов: {episodes}\n'
            f'Статус: {status}\n'
            f'Студия: {studio}\n'
            '========================\n'
            '<b>🔔 Теперь вы отслеживаете это аниме!</b>', reply_markup=markup)
            db.setTracking(db.getId(message.from_user.id), link) # Выставляем ссылку в запись пользователя
            db.setEpisodes(db.getId(message.from_user.id), parser.getEpisodes(db.getTracking(db.getId(message.from_user.id)))) # Туда же количество эпизодов
        else:
            bot.send_photo(message.from_user.id, requests.get(thumbnail).content, f'<b>{title}</b> \n'
            '========================\n'
            f'Эпизодов: {episodes}\n'
            f'Статус: {status}\n'
            f'Студия: {studio}\n'
            '========================\n'
            '<b>⚠️ Вы не можете отслеживать это аниме!</b>', reply_markup=markup)

def userExists(userId):
    lock.acquire(False) # Получаем лок нашего потока, чтобы sqlite3 не ругался на рекурсивное обращение к БД
    try:
        if(not db.userExists(userId)): # Создаём запись о пользователе, если его ещё не существует
            db.addUser(userId)
    finally:
        lock.release() # Отпускаем лок, чтобы проверка могла работать дальше


bot.polling(none_stop=True, interval=0)


