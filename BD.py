import sqlite3
from random import randint

import time
import datetime

import telebot
from flask import Flask, request

bot = telebot.TeleBot('5571697367:AAEzZIlfkW-WAPmW0spsPBd-gnUAcq7pb-U')
app = Flask(__name__)

@bot.message_handler(['start'])
def start(message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
    id INT,
    name STR, 
    score INT
    )""")
    connect.commit()

    people_id = message.from_user.id
    name = message.from_user.first_name
    cursor.execute(f"SELECT id FROM users WHERE id = {people_id}")
    data = cursor.fetchone()
    if data is None:
        cursor.execute(f"INSERT INTO users VALUES(?,?,?);", (people_id, name, 0))
        connect.commit()

    photo = open('photo_start.jpg', 'rb')
    bot.send_photo(message.chat.id, photo)

@bot.message_handler(['help'])
def help(message):
    photo = open('photo_help.jpg', 'rb')
    bot.send_photo(message.chat.id, photo)

@bot.message_handler(['dick'])
def dick(message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    people_id = message.from_user.id
    name = message.from_user.first_name
    cursor.execute(f"SELECT id FROM users WHERE id = {people_id}")
    data = cursor.fetchone()
    if data is None:
        cursor.execute(f"INSERT INTO users VALUES(?,?,?);", (people_id, name, 0))
        connect.commit()

    number = randint(-5, 10)
    cursor.execute(f"SELECT score FROM users WHERE id = {people_id}")
    score1 = cursor.fetchone()[0]
    cursor.execute(f"UPDATE users SET score = {number + score1} WHERE id = {people_id}")
    connect.commit()

    mes = f'{name}, твой писюн сократился на {number} см. Теперь он равен {number + score1} см. Следующая попытка через 12 часов :('
    if number == -5:
        bot.send_message(message.chat.id, mes)
    elif number == -4:
        bot.send_message(message.chat.id, mes)
    elif number == -3:
        bot.send_message(message.chat.id, mes)
    elif number == -2:
        bot.send_message(message.chat.id, mes)
    elif number == -1:
        bot.send_message(message.chat.id, mes)
    else:
        bot.send_message(message.chat.id, f'{name}, твой писюн вырос на {number} см. Теперь он равен {number + score1} см. Следующая попытка через 12 часов! :3')



@bot.message_handler(['stats'])
def stats(message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute(f"SELECT name FROM users")
    name = cursor.fetchall()
    cursor.execute(f"SELECT score FROM users")
    data = cursor.fetchall()

    for i in range(len(data)):
        list = (str(name[i][0]) + ':  ' + str(data[i][0]))
        bot.send_message(message.chat.id, f'{list}', parse_mode='html')

#@app.route("/" + '5571697367:AAEzZIlfkW-WAPmW0spsPBd-gnUAcq7pb-U', methods=['POST'])
#def getMessage():
    #bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    #return "!", 200

#bot.remove_webhook()
#bot.set_webhook('https://test.com' + '5571697367:AAEzZIlfkW-WAPmW0spsPBd-gnUAcq7pb-U')
#app.run()

bot.polling()