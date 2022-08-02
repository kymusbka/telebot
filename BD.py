import telebot
import sqlite3
from random import randint

bot = telebot.TeleBot('5571697367:AAEzZIlfkW-WAPmW0spsPBd-gnUAcq7pb-U')

@bot.message_handler(['start'])
def start(message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
    id INT, 
    score INT
    )""")
    connect.commit()

    people_id = message.from_user.id
    cursor.execute(f"SELECT id FROM users WHERE id = {people_id}")
    data = cursor.fetchone()
    if data is None:
        cursor.execute(f"INSERT INTO users VALUES(?,?);", (people_id, 0))
        connect.commit()

@bot.message_handler(['dick'])
def dick(message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    people_id = message.from_user.id
    cursor.execute(f"SELECT id FROM users WHERE id = {people_id}")
    data = cursor.fetchone()
    if data is None:
        cursor.execute(f"INSERT INTO users VALUES(?,?);", (people_id, 0))
        connect.commit()
    number = randint(-5, 10)
    cursor.execute(f"SELECT score FROM users WHERE id = {people_id}")
    score1 = cursor.fetchone()[0]
    cursor.execute(f"UPDATE users SET score = {number + score1} WHERE id = {people_id}")
    connect.commit()
    bot.send_message(message.chat.id, number)

@bot.message_handler(['stats'])
def stats(message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute('SELECT score FROM users')
    data = cursor.fetchone()[0]
    name = message.from_user.first_name
    for i in range(len(data)):
        bot.send_message(message.chat.id, )

bot.polling()