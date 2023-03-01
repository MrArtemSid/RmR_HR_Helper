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


class UserInfo:
    def __init__(self, num_of_ans, level, type_of_q, prev_ans, q_id, cnt_correct):
        self.num_of_ans = num_of_ans
        self.level = level
        self.type_of_q = type_of_q
        self.prev_ans = prev_ans
        self.q_id = q_id
        self.cnt_correct = cnt_correct

    num_of_ans = 0  # количество ответов
    level = 0  # уровень блока вопросов
    type_of_q = "type"  # тип вопроса
    prev_ans = ""  # предыдущий ответ пользователя
    q_id = 0  # номер текущего вопроса
    cnt_correct = 0 # количество верных ответов

def get_result(message, user_id):
    if levels[user_id].num_of_ans >= config.cnt_questions:
        levels[user_id].num_of_ans = 0
        if levels[user_id].cnt_correct >= config.correct_ans:
            if levels[user_id].level in [2, 4]:
                is_yes_to_start[user_id] = 0
                text = "Вы ответили правильно на " + str(levels[user_id].cnt_correct / (
                            config.cnt_questions * 2) * 100) + "% вопросов\nНажмите /start для повторной попытки"
                bot.send_message(message.from_user.id,
                                 text)
                levels.pop(user_id)
                used.pop(user_id)
            else:
                bot.send_message(message.from_user.id,
                                 "Я удивлен вашим познаниям. Давайте узнаем на что вы действительно способны")
            if user_id in levels:
                levels[user_id].level += 1
        else:
            text = "Вы ответили правильно на " + str(levels[user_id].cnt_correct / config.cnt_questions * 100) \
                   + "% вопросов первого теста\n Вам следует серьезнее подготовиться, иначе можно завалить КТ\nНажмите /start для повторной попытки"
            bot.send_message(message.from_user.id, text)
            is_yes_to_start[user_id] = 0
        if user_id in levels and user_id in used:
            levels[user_id].prev_ans = ""
            used[user_id] = []

def get_prev_correct_answer(user_id, level):
    prev_corr_ans = ""
    if levels[user_id].prev_ans != "":
        tmp = "!" + levels[user_id].prev_ans
        for ans in questions[level][used[user_id][-1]][2:]:
            if ans[0] == "!":
                prev_corr_ans = "Вы неверно ответили на предыдущий вопрос. Правильный ответ - " + ans[1:]
            if tmp == ans:
                prev_corr_ans = ""
                levels[user_id].cnt_correct += 1
                break
    return prev_corr_ans

def init_new_task(user_id, level, rand1, markup):
    used[user_id].append(rand1)
    s1 = questions[level][rand1][0]
    type_q = questions[level][rand1][1]
    levels[user_id].type_of_q = type_q
    if type_q == "keys":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for i in range(len(questions[level][rand1][2:])):
            tmp = questions[level][rand1][2:][i]
            if tmp[0] == '!':
                tmp = tmp[1:]
            markup.add(types.KeyboardButton(tmp))
    return s1, markup


@bot.message_handler(commands=['start'])
# Спрашиваем человека готов ли он к собеседованию
def st(message):
    user_id = str(message.from_user.id)
    is_yes_to_start[user_id] = 0
    levels[user_id] = UserInfo(0, 0, 'type', "", 0,
                               0)
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
            levels[user_id] = UserInfo(0, 0, 'type', "", 0,
                                       0)  # количество ответов, уровень блока вопросов, тип вопроса, количество верных ответов
        if user_id not in used:
            used[user_id] = []
        else:
            if levels[user_id].type_of_q == "keys":
                levels[user_id].prev_ans = message.text
        level = levels[user_id].level
        get_result(message, user_id)
        if user_id in levels:
            level = levels[user_id].level
        if len(questions[level]) > 0 and is_yes_to_start[user_id] != 0:
            if levels[user_id].level == 0:
                rand1 = levels[user_id].q_id
            if levels[user_id].level != 0:
                rand1 = randint(0, len(questions[level]) - 1)
                while rand1 in used[user_id]:
                    rand1 = randint(0, len(questions[level]) - 1)
                else:
                    levels[user_id].num_of_ans += 1
            if levels[user_id].level == 0:
                levels[user_id].q_id = rand1 + 1
                if (levels[user_id].q_id > len(questions[level])):
                    # if (message.text == '8'):
                    level = 1
                    levels[user_id].level = level
                    levels[user_id].num_of_ans = 1
                    levels[user_id].prev_ans = ""
                    used[user_id] = []
                    rand1 = randint(0, len(questions[level]) - 1)

            prev_corr_ans = get_prev_correct_answer(user_id, level)
            s1, markup = init_new_task(user_id, level, rand1, markup)

    print("Пользователь написал: ", '"', message.text, '"', sep='')
    if s1 != '.' and is_yes_to_start[user_id] != 0:
        if (len(prev_corr_ans) > 0):
            bot.send_message(message.from_user.id, prev_corr_ans, reply_markup=markup)
        msg = bot.send_message(message.from_user.id, s1, reply_markup=markup)
        print("Бот написал: ", '"', s1, '"', sep='')
    sys.stdout = open(filename, 'a')


bot.polling()
