import telebot
import requests
import json

bot = telebot.TeleBot('7069309590:AAFfn7prjochFh-SZLhFeH1iw0POtSfd5JA')

API = '05ee88e75f48ecfba5f55910ec5c193c'


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Salom, shahar nomini kiriting: ')

@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    if res.status_code == 200:
        data = json.loads(res.text)
        temp = data["main"]["temp"]
        bot.reply_to(message, f'At this moment weather is: {temp}')

        img = 'sunny.jpg' if temp > 5.0 else 'sun.jpg'
        file = open('./img/' + img, 'rb')
        bot.send_photo(message.chat.id, file)

    else:
        bot.reply_to(message, f'Not Found: 404')

bot.polling(none_stop=True)