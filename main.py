# Питоновские библиотеки
import telebot
import requests
import sys
from os import mkdir, path, remove, stat
from telebot import types
from random import randint

# Cвои библиотеки
from config import token
import config
import convert
from questions import questions
used = {}
levels = {}

bot = telebot.TeleBot(token)
print("Бот работает")
is_yes_to_start = dict()

@bot.message_handler(commands=['start'])
# Спрашиваем человека готов ли он к собеседованию
def st(message):
    user_id = str(message.from_user.id)
    is_yes_to_start[user_id] = 0
    levels[user_id] = [0, 0, 'type', [], 0, 'passed'] # количество ответов, уровень блока вопросов, тип вопроса, ответы
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
    flag_for_keys = 0
    if user_id not in is_yes_to_start:
        is_yes_to_start[user_id] = 0
    if is_yes_to_start[user_id] == 0:
        if message.text.lower() == "нет":
            s1 = "Грустно( пишите /start, как будете готовы"
        elif message.text.lower() == "да":
            s1 = "Хорошо, начнём"
            is_yes_to_start[user_id] = 1
        bot.send_message(message.from_user.id,
                         s1)
    if is_yes_to_start[user_id] == 1:
        if user_id not in levels:
            levels[user_id] = [0, 0, 'type', [], 0, 'passed'] # количество ответов, уровень блока вопросов, тип вопроса, ответы
        if user_id not in used:
            used[user_id] = []
        else:
            if levels[user_id][2] == "keys":
                levels[user_id][3].append(message.text)
        level = levels[user_id][1]
        if levels[user_id][0] >= config.cnt_questions:
            levels[user_id][0] = 1
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
                                     "Мы переходим к финальному этапу нашего собеседования")
                else:
                    bot.send_message(message.from_user.id,
                                     "Я удивлен вашим познаниям. Давайте узнаем на что вы действительно способны")
                levels[user_id][1] += 1
            else:
                bot.send_message(message.from_user.id, "Спасибо за проходение тестирования ! Мы вам перезвоним.")
                is_yes_to_start[user_id] = 0
            levels[user_id][3] = []
            used[user_id] = []
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
                bot.send_message(message.chat.id, s1, reply_markup=markup)
                print("Бот написал: ", '"', s1, '"', sep='')
                flag_for_keys = 1


    if s1 != '.' and not flag_for_keys and is_yes_to_start[user_id] != 0:
        flag_for_keys = 0
        bot.send_message(message.from_user.id, s1)
        print("Бот написал: ", '"', s1, '"', sep='')

    print("Пользователь написал: ", '"', message.text, '"', sep='')
    sys.stdout = open(filename, 'a')


@bot.message_handler(content_types=['voice'])
def get_voice_messages(message):
    user_id = str(message.from_user.id)
    folder_name = user_id
    if not path.exists(folder_name):
        mkdir(folder_name)
    file_info = bot.get_file(message.voice.file_id)
    filename = folder_name + '/' + file_info.file_path[6:]
    file = requests.get('https://api.telegram.org/file/bot{0}/{1}'.format(token, file_info.file_path))

    with open(filename, 'wb') as f:
        f.write(file.content)

    src_filename = filename
    dest_filename = filename[:-4] + ".wav"
    convert.oga_to_wav(src_filename, dest_filename)
    remove(src_filename)
    if (stat(dest_filename).st_size) < 1024 * 1024:  # Яндекс не распознает аудиофайлы больше 1 МБ.
        text_from_voice = convert.voice_to_text_yandex(dest_filename)
    else:
        text_from_voice = convert.voice_to_text_google(dest_filename)
    filename = folder_name + '/' + 'user_input.txt'
    sys.stdout = open(filename, 'a')
    if len(text_from_voice) > 0:
        bot.send_message(message.from_user.id, 'Ваше голосовое сообщение было распознано как: \n\n' + text_from_voice)
        print("Пользователь сказал(голосовая #{}): ".format(file_info.file_path[11:-4]), text_from_voice)
    else:
        bot.send_message(message.from_user.id, "не понимаю, не услышал вас")
        print("Бот не смог распознать речь или она отсутствовала(голосовая #{})".format(file_info.file_path[11:-4]))
    sys.stdout = open(filename, 'a')


bot.polling()
