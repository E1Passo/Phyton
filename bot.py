# bot
import pyowm
import telebot
import json

owm = pyowm.OWM('65ec49edc4b116d2bd5a68749ea33b2b')
bot = telebot.TeleBot("1334344826:AAF4-76AvRA-rl4XA4K07XAhbxJ0LpyRhzQ")

keyboard1 = telebot.types.ReplyKeyboardMarkup(True)
keyboard1.row('Москва', 'Санкт-Петербург', 'Краснодар', 'Челябинск')


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, это телеграмм бот который показывает погоду в любом городе.'
                                      ' Просто напиши город и получай результат!', reply_markup=keyboard1)


@bot.message_handler(commands=['start', 'help'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, это телеграмм бот который показывает погоду в любом городе.'
                                      ' Просто напиши город и получай результат!', reply_markup=keyboard1)


@bot.message_handler(content_types=["text"])
def send_echo(message):
    mgr = owm.weather_manager()
    try:
        observation = mgr.weather_at_place(message.text)
    except pyowm.commons.exceptions.NotFoundError:
        result = f"Города {message.text} в базе нет!"
        bot.send_message(message.chat.id, result, reply_markup=keyboard1)

        with open("log.txt", "a") as file_object:
            file_object.write(message.text + '\n')
        print(message.text)

    else:
        w = observation.weather
        temp = w.temperature('celsius')["temp"]

        result = "В городе " + message.text + " - " + "сейчас " + w.detailed_status + "\n"
        result += "Температура сейчас в районе " + str(temp) + " градусов " + "\n\n"

        if temp < 10.0:
            result += "Сейчас очень холодно, надевай шубу!"
        elif temp < 20.0:

            result += "Сейчас  холодно, одевайся теплее."
        else:
            result += "Очень жарко, надевай плавки."

        bot.send_message(message.chat.id, result, reply_markup=keyboard1)


bot.polling(none_stop=True)
