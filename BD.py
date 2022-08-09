import sqlite3
from random import randint
import datetime
import telebot


bot = telebot.TeleBot('5571697367:AAEzZIlfkW-WAPmW0spsPBd-gnUAcq7pb-U')

mess_time = datetime.date.today()

@bot.message_handler(['start'])
def start(message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
    id INT,
    name STR, 
    score INT,
    kd INT
    )""")
    connect.commit()

    people_id = message.from_user.id
    name = message.from_user.first_name
    cursor.execute(f"SELECT id FROM users WHERE id = {people_id}")
    data = cursor.fetchone()
    if data is None:
        cursor.execute(f"INSERT INTO users VALUES(?,?,?,?);", (people_id, name, 0, 0))
        connect.commit()

    bot.send_message(message.chat.id, 'Смысл бота: '
                                      '\n\nИгрок может прописывать команду /dick, '
                                      '\nгде в ответ получит от бота рандомное возвышение... '
                                      '\nего виртуального пинуса ^-^'
                                      '\nВсего в сумме дается по две попытки на день.'
                                      '\nРандом работает от -5 см до +10 см, но есть и другие вероятности)'
                                      '\n\nЕсли у тебя есть вопросы — пиши команду: /help')

@bot.message_handler(['help'])
def help(message):
    bot.send_message(message.chat.id, 'Команды бота: '
                                      '\n\n/dick — Вырастить/уменьшить пипису '
                                      '\n/stats — Статистика')

@bot.message_handler(['dick'])
def dick(message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    people_id = message.from_user.id
    name = message.from_user.first_name
    cursor.execute(f"SELECT id FROM users WHERE id = {people_id}")
    data = cursor.fetchone()
    if data is None:
        cursor.execute(f"INSERT INTO users VALUES(?,?,?,?);", (people_id, name, 0, 0))
        connect.commit()

    global mess_time
    cursor.execute(f"SELECT kd FROM users WHERE id = {people_id}")
    kd = cursor.fetchone()[0]
    num = 1
    if mess_time != datetime.date.today():
        cursor.execute(f"UPDATE users SET kd = {0} WHERE id = {people_id}")
        connect.commit()
    if kd >= 2:
        bot.send_message(message.chat.id, f'{name}, твой лимит исчерпан. '
                                          f'\nСледующая попытка завтра!')
    else:
        cursor.execute(f"UPDATE users SET kd = {kd + num} WHERE id = {people_id}")
        cursor.execute(f"SELECT score FROM users WHERE id = {people_id}")
        score1 = cursor.fetchone()[0]
        number = randint(-5, 10)
        random1 = randint(1, 100)
        random2 = randint(1, 1000)

        if score1 == 0:
            number2 = randint(0, 10)
            cursor.execute(f"UPDATE users SET score = {number2 + score1} WHERE id = {people_id}")
            connect.commit()
            bot.send_message(message.chat.id, f'{name}, твой писюн вырос на {number2} см :3'
                                              f'\nТеперь он равен {number2 + score1} см')
        elif random1 == 14:
            minus1 = -15
            cursor.execute(f"UPDATE users SET score = {number + score1} WHERE id = {people_id}")
            connect.commit()
            bot.send_message(message.chat.id, f'{name}, твой писюн сократился на {minus1} см :('
                                              f'\nТеперь он равен {minus1 + score1} см')
        elif random2 == 583:
            minus2 = -30
            cursor.execute(f"UPDATE users SET score = {number + score1} WHERE id = {people_id}")
            connect.commit()
            bot.send_message(message.chat.id, f'{name}, твой писюн сократился на {minus2} см :('
                                              f'\nТеперь он равен {minus2 + score1} см')
        elif number < 0:
            cursor.execute(f"UPDATE users SET score = {number + score1} WHERE id = {people_id}")
            connect.commit()
            bot.send_message(message.chat.id, f'{name}, твой писюн сократился на {number} см :('
                                              f'\nТеперь он равен {number + score1} см')
        else:
            cursor.execute(f"UPDATE users SET score = {number + score1} WHERE id = {people_id}")
            connect.commit()
            bot.send_message(message.chat.id, f'{name}, твой писюн вырос на {number} см :3 '
                                              f'\nТеперь он равен {number + score1} см')


@bot.message_handler(['stats'])
def stats(message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute("SELECT name FROM users")
    name = cursor.fetchall()
    cursor.execute("SELECT score FROM users")
    score = cursor.fetchall()

    for i in range(len(name)):
        bot.send_message(message.chat.id, str(name[i][0]) + ':  ' + str(score[i][0]))

bot.polling(none_stop=True)