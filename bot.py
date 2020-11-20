# coding=utf-8
import requests
import config
import telebot
import datetime
from bs4 import BeautifulSoup
from typing import List, Tuple

bot = telebot.TeleBot(config.access_token)


# telebot.apihelper.proxy = {'https': 'https://104.248.53.46:3128'}


@bot.message_handler(commands=['start'])
def start(message: str):
    bot.send_message(message.chat.id,
                     "Привет! Чтобы начать получать рассылку с уведомлениями о предстоящих парах - отправь в чат команду /add_user XXXXX, где ХХХХХ - номер твоей группы. Первая буква - заглавная латинская!")


@bot.message_handler(commands=['add_user'])
def add_new_student(message: str):
    print(message.text[10:], message.chat.id)

    bot.send_message(message.chat.id, "Отлично!")
    # print(message.chat.id)


'''

bot.message_handler(commands=['near_lesson'])
def get_near_lesson(message: str) -> None:
    _, group = message.text.split()
    weekday = datetime.datetime.today().weekday() + 1
    week = get_week()
    web_page = get_page(group, week)
    if web_page is None:
        bot.send_message(message.chat.id, "Группа введена неправильно", parse_mode='HTML')
    else:
        flag = 0
        current_schedule = get_schedule(web_page, weekday)
        if current_schedule:
            times_lst, locations_lst, lessons_lst = current_schedule
            a = str(datetime.datetime.now().time())
            b = int(a[0:2] + a[3:5]) #Текущее время
            for i in range(len(times_lst)):
                if b < int(times_lst[i][6:8] + times_lst[i][9:11]):
                    resp = ''
                    resp += '<b>{}</b>, {}, {}\n'.format(times_lst[i], locations_lst[i], lessons_lst[i])
                    bot.send_message(message.chat.id, resp, parse_mode='HTML')
                    flag = 1
                    break
        if flag == 0:            
            while True:
                if weekday == 7:
                    weekday = 1
                    if week == 1:
                        week = 2
                    else:
                        week = 1
                else:
                    weekday += 1

                current_schedule = get_schedule(web_page, weekday)
                if current_schedule:
                    times_lst, locations_lst, lessons_lst = current_schedule
                    resp = ''
                    resp += '<b>{}</b>, {}, {}\n'.format(times_lst[0], locations_lst[0], lessons_lst[0])
                    bot.send_message(message.chat.id, resp, parse_mode='HTML')
                    break

'''

if __name__ == '__main__':
    bot.polling()


