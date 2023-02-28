# Питоновские библиотеки
import telebot
import requests
import sys
from os import mkdir, path, remove, stat
from telebot import types
from random import randint

# Cвои библиотеки
import config
from questions import questions
used = {}
levels = {}
names = {}

bot = telebot.TeleBot(config.token)
print("Бот работает")
is_yes_to_start = dict()
@bot.message_handler(commands=['start'])
# Спрашиваем человека готов ли он к собеседованию
def st(message):
    user_id = str(message.from_user.id)
    is_yes_to_start[user_id] = 0
    levels[user_id] = [0, 1, 'type', [], 0, 'passed'] # количество ответов, уровень блока вопросов, тип вопроса, ответы
    used[user_id] = []

    folder_name = user_id
    if not path.exists(folder_name):
        mkdir(folder_name)
    filename = folder_name + '/' + 'user_input.txt'
    sys.stdout = open(filename, 'a')

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("Да")
    button2 = types.KeyboardButton("Нет")
    markup.add(button1, button2)

    s1 = "Привет, {0.first_name}! Вы готовы начать собеседование ?".format(message.from_user)

    bot.send_message(message.chat.id, s1, reply_markup=markup)
    print("Бот написал: ", '"', s1, '"', sep='')

    sys.stdout = open(filename, 'a')

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    user_id = str(message.from_user.id)
    folder_name = user_id
    if not path.exists(folder_name):
        mkdir(folder_name)
    filename = folder_name + '/' + 'user_input.txt'
    sys.stdout = open(filename, 'a')

    s1 = '.'
    markup = types.ReplyKeyboardRemove(selective=False)
    if user_id not in is_yes_to_start:
        is_yes_to_start[user_id] = 0
    if is_yes_to_start[user_id] == 0:
        if message.text.lower() == "нет":
            s1 = "Грустно( пишите /start, как будете готовы"
        elif message.text.lower() == "да":
            s1 = "Хорошо, начнём"
            is_yes_to_start[user_id] = 1
        if s1 != '.':
            bot.send_message(message.from_user.id,
                         s1)
    if is_yes_to_start[user_id] == 1:
        if user_id not in levels:
            levels[user_id] = [0, 1, 'type', [], 0, 'passed'] # количество ответов, уровень блока вопросов, тип вопроса, ответы
        if user_id not in used:
            used[user_id] = []
        else:
            if levels[user_id][2] == "keys":
                levels[user_id][3].append(message.text)
        level = levels[user_id][1]
        if levels[user_id][0] >= config.cnt_questions:
            levels[user_id][0] = 0
            cnt_correct = 0
            for i in range(len(used[user_id])):
                curr_block = questions[levels[user_id][1]] # узнаем блок
                for corr_ans in curr_block[used[user_id][i]]: # ответы нужного вопроса
                    if corr_ans[0] == "!":
                        corr_ans = corr_ans[1:]
                        break
                if corr_ans == levels[user_id][3][i]:
                    cnt_correct += 1
            if cnt_correct >= config.correct_ans:
                if levels[user_id][1] in [2, 4]:
                    is_yes_to_start[user_id] = 0
                    bot.send_message(message.from_user.id,
                                     config.success_message)
                    specification = ''
                    if levels[user_id][1] == 2:
                        specification = "DataScience"
                    elif levels[user_id][1] == 4:
                        specification = "FrontEnd"
                    username = message.from_user.username
                    first_name = message.from_user.first_name
                    pr1 = str(user_id) + "|" + str(username) + " - " + str(first_name) + "|" + str(specification) + "|" + "passed"
                    requests.get("https://hr-hackaton.herokuapp.com/hr/addUser?pr1={}".format(pr1))
                    levels.pop(user_id)
                    used.pop(user_id)
                else:
                    bot.send_message(message.from_user.id,
                                     "Я удивлен вашим познаниям. Давайте узнаем на что вы действительно способны")
                if user_id in levels:
                    levels[user_id][1] += 1
            else:
                bot.send_message(message.from_user.id, config.failed_message)
                specification = ''
                if levels[user_id][1] == 1:
                    bot.send_message(message.from_user.id, "Чтобы не терять время напрасно предлагаем вам курсы от нашего партнера\n\n" + config.datascience_ad)
                    specification = "DataScience"
                elif levels[user_id][1] == 3:
                    bot.send_message(message.from_user.id,
                                     "Чтобы не терять время напрасно предлагаем вам курсы от нашего партнера\n\n" + config.frontend_ad)
                    specification = "FrontEnd"

                username = message.from_user.username
                first_name = message.from_user.first_name
                pr1 = str(user_id) + "|" + str(username) + " - " + str(first_name) + "|" + str(specification) + "|" + "failed"
                requests.get("https://hr-hackaton.herokuapp.com/hr/addUser?pr1={}".format(pr1))
                is_yes_to_start[user_id] = 0
            if user_id in levels and user_id in used:
                levels[user_id][3] = []
                used[user_id] = []
        if user_id in levels:
            level = levels[user_id][1]
        if len(questions[level]) > 0 and is_yes_to_start[user_id] != 0:
            if levels[user_id][1] == 0:
                rand1 = levels[user_id][4]
            if levels[user_id][1] != 0:
                rand1 = randint(0, len(questions[level]) - 1)
                while rand1 in used[user_id]:
                    rand1 = randint(0, len(questions[level]) - 1)
                else:
                    levels[user_id][0] += 1
            if levels[user_id][1] == 0:
                if levels[user_id][4] == 2 and message.text.lower() == "нет":
                    rand1 = 3
                levels[user_id][4] = rand1 + 1
                if (levels[user_id][4] > len(questions[level])):
                    if (message.text == 'DATA SCIENTIST'):
                        level = 1
                    else:
                        level = 3
                    levels[user_id][1] = level
                    levels[user_id][0] = 1
                    levels[user_id][3] = []
                    used[user_id] = []
                    rand1 = randint(0, len(questions[level]) - 1)

            used[user_id].append(rand1)
            s1 = questions[level][rand1][0]
            type_q = questions[level][rand1][1]
            levels[user_id][2] = type_q
            if type_q == "keys":
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                for i in range(len(questions[level][rand1][2:])):
                    tmp = questions[level][rand1][2:][i]
                    if tmp[0] == '!':
                        tmp = tmp[1:]
                    markup.add(types.KeyboardButton(tmp))

    print("Пользователь написал: ", '"', message.text, '"', sep='')
    if s1 != '.' and is_yes_to_start[user_id] != 0:
        msg = bot.send_message(message.from_user.id, s1, reply_markup=markup)
        print("Бот написал: ", '"', s1, '"', sep='')
    sys.stdout = open(filename, 'a')


bot.polling()
