# Телеграм бот "Погода"_2
import telebot                                                      # Импорт модуля telebot для создания и управления ботами в Telegram.
import requests                                                     # Импорт модуля requests для отправки HTTP-запросов.
import json                                                         # Импорт модуля json для работы с JSON-данными.
from telebot import types                                           # Импорт модуля types из telebot для использования типов сообщений бота.

bot = telebot.TeleBot(token='YOUR TOKEN')                           # Создание экземпляра бота с указанным токеном.
API_OpenWeather = 'YOUR API'                                        # API-ключ для OpenWeatherMap (https://openweathermap.org/)
temp = None                                                         # Переменная для хранения текущей температуры.
feels_like = None                                                   # Переменная для хранения ощущаемой температуры.
temp_min = None                                                     # Переменная для хранения минимальной температуры.
temp_max = None                                                     # Переменная для хранения максимальной температуры.
pressure = None                                                     # Переменная для хранения давления.
humidity = None                                                     # Переменная для хранения влажности.
visibility = None                                                   # Переменная для хранения видимости.
description = None                                                  # Переменная для хранения описания погоды.

@bot.message_handler(commands=['start'])                            # Обработчик команды '/start'.
def start(message):                                                 # Отправка приветственного сообщения и инструкций.
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name} {message.from_user.last_name}! 🤝\n'
                                      f'Напиши название города для получения данных о температуре')

@bot.message_handler(content_types=['text'])                        # Обработчик текстовых сообщений.
def get_city(message):
    city = message.text.strip().lower()                             # Получение названия города из сообщения и приведение его к нижнему регистру.
    global temp, feels_like, temp_min, temp_max, pressure, humidity, visibility, description  # Объявление глобальных переменных для хранения данных о погоде.
    response = requests.get(                                        # Отправка запроса к API OpenWeatherMap для получения данных о погоде для указанного города.
        f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_OpenWeather}&units=metric&lang=ru')

    if response.status_code == 200:                                 # Если запрос успешен (статус код 200):
        data = json.loads(response.content)                         # Преобразование полученных данных в формат JSON.

        # Извлечение необходимых данных из JSON-ответа.
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        temp_min = data['main']['temp_min']
        temp_max = data['main']['temp_max']
        pressure = data['main']['pressure']
        humidity = data['main']['humidity']
        visibility = data['visibility']
        description = data['weather'][0]['description']

        # Создание клавиатуры с вариантами выбора данных о погоде.
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Температура 🌡', callback_data='temperature'))
        markup.add(types.InlineKeyboardButton('Восприятие температуры 🌡', callback_data='feels_like'))
        markup.add(types.InlineKeyboardButton('Минимальная температура ↘️', callback_data='temp_min'))
        markup.add(types.InlineKeyboardButton('Максимальная температура ⬆️', callback_data='temp_max'))
        markup.add(types.InlineKeyboardButton('Давление 🔴', callback_data='pressure'))
        markup.add(types.InlineKeyboardButton('Влажность 💧', callback_data='humidity'))
        markup.add(types.InlineKeyboardButton('Видимость 🔭', callback_data='visibility'))
        markup.add(types.InlineKeyboardButton('Состояние ☀️', callback_data='description'))

        bot.send_message(message.chat.id, 'Данные получены. Выберите нужное:', reply_markup=markup)  # Отправка сообщения с вариантами выбора данных о погоде.

    else:                                                               # Если запрос не успешен:
        bot.reply_to(message, f'Неверное написание города - {city} 🙈')  # Отправка ответного сообщения о неверном написании города.

def emoji(description):
    if description == 'пасмурно':                                       # Если описание погоды - 'пасмурно':
        return '⛅️'                                                     # Возвращаем соответствующую эмодзи.
    if description == 'облачно с прояснениями':                         # Если описание погоды - 'облачно с прояснениями':
        return '🌤️'                                                     # Возвращаем соответствующую эмодзи.
    if description == 'небольшая облачность':                           # Если описание погоды - 'небольшая облачность':
        return '🌤️'                                                     # Возвращаем соответствующую эмодзи.
    if description == 'ясно':                                           # Если описание погоды - 'ясно':
        return '☀️️'                                                     # Возвращаем соответствующую эмодзи.
    if description == 'небольшой дождь':                                # Если описание погоды - 'небольшой дождь':
        return '🌧'                                                      # Возвращаем соответствующую эмодзи
    if description == 'дождь':                                          # Если описание погоды - 'дождь':
        return '🌧'                                                      # Возвращаем соответствующую эмодзи

@bot.callback_query_handler(func=lambda call: True)                     # Обработчик коллбэк-запросов.
def show_callback(call):
    if call.data == 'temperature':                                      # Если выбрана опция 'Температура':
        bot.send_message(call.message.chat.id, f'Сейчас погода: {temp} градус(а)ов')  # Отправка сообщения с текущей температурой.
    elif call.data == 'feels_like':                                     # Если выбрана опция 'Восприятие температуры':
        bot.send_message(call.message.chat.id, f'Ощущается как: {feels_like} градус(а)ов')  # Отправка сообщения с ощущаемой температурой.
    elif call.data == 'temp_min':                                       # Если выбрана опция 'Минимальная температура':
        bot.send_message(call.message.chat.id, f'Минимальная температура: {temp_min} градус(а)ов')  # Отправка сообщения с минимальной температурой.
    elif call.data == 'temp_max':                                       # Если выбрана опция 'Максимальная температура':
        bot.send_message(call.message.chat.id, f'Максимальная температура: {temp_max} градус(а)ов')  # Отправка сообщения с максимальной температурой.
    elif call.data == 'pressure':                                       # Если выбрана опция 'Давление':
        bot.send_message(call.message.chat.id, f'Давление: {pressure} ртутного столба')  # Отправка сообщения с данными о давлении.
    elif call.data == 'humidity':                                       # Если выбрана опция 'Влажность':
        bot.send_message(call.message.chat.id, f'Влажность: {humidity}')  # Отправка сообщения с данными о влажности.
    elif call.data == 'visibility':                                     # Если выбрана опция 'Видимость':
        bot.send_message(call.message.chat.id, f'Видимость: {visibility} метров')  # Отправка сообщения с данными о видимости.
    elif call.data == 'description':                                    # Если выбрана опция 'Состояние':
        bot.send_message(call.message.chat.id, f'Состояние: {description} {emoji(description)}')  # Отправка сообщения с данными о состоянии погоды и соответствующей эмодзи.

bot.polling(none_stop=True)                                             # Запуск процесса получения и обработки сообщений бота.
