import telebot
import sqlite3

name = None

bot = telebot.TeleBot('7069309590:AAFfn7prjochFh-SZLhFeH1iw0POtSfd5JA')

@bot.message_handler(commands=['start'])
def start(message):
    conn = sqlite3.connect('wrs.sql')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key , name varchar(50), pass varchar(50))')
    conn.commit()
    cur.close()
    conn.close()



    bot.send_message(message.chat.id, 'Hi, Enter your name: ')
    bot.register_next_step_handler(message, user_name)

def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, 'Enter PASS')
    bot.register_next_step_handler(message, user_pass)

def user_pass(message):
    password = message.text.strip()

    conn = sqlite3.connect('wrs.sql')
    cur = conn.cursor()

    cur.execute("INSERT INTO users (name, pass) VALUES ('%s', '%s')" % (name, password))
    conn.commit()
    cur.close()
    conn.close()

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton('Users', callback_data='users'))
    bot.send_message(message.chat.id, 'Regist', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    conn = sqlite3.connect('wrs.sql')
    cur = conn.cursor()

    cur.execute('SELECT * FROM users')
    users = cur.fetchall()

    info = ''
    for el in users:
        info += f'Name: {el[1]}, Pass: {el[2]} \n'
    cur.close()
    conn.close()

    bot.send_message(call.message.chat.id, info)

bot.polling(none_stop=True)