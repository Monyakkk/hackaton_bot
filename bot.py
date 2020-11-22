# coding=utf-8
import requests
import config
import telebot
import re
import datetime as DT
import time
from bs4 import BeautifulSoup
from typing import List, Tuple
from DB import Groups, Timetable, session

bot = telebot.TeleBot(config.access_token)
AllGroups = ['K3241', 'M3208']

# telebot.apihelper.proxy = {'https': 'https://104.248.53.46:3128'}


@bot.message_handler(commands=['start'])
def start(message: str):
    
    bot.send_message(message.chat.id,
                     "Привет! Чтобы начать получать рассылку с уведомлениями о предстоящих парах - отправь в чат команду /add_user XXXXX, где ХХХХХ - номер твоей группы. Первая буква - заглавная латинская!")


@bot.message_handler(commands=['add_user'])
def add_new_student(message: str):

    s=session()
    rows = s.query(Groups).filter(Groups.TelegramID == message.chat.id).all()
    
    if len(rows)>0:
        
        bot.send_message(message.chat.id, "Ты уже зарегистрирован как студент группы " + s.query(Groups).get(message.chat.id).GroupID + ". Вы можете отписаться от рассылки этой группы командой /remove_user")
        return None
    else:
        if message.text[10:] in AllGroups: 
            NewUser = Groups(GroupID=message.text[10:], TelegramID=message.chat.id)
            s.add(NewUser)
            s.commit()         
            bot.send_message(message.chat.id, "Отлично! Теперь вы зарегистрированы как студент группы " + message.text[10:] + ". Чтобы получить полный список команд для бота - напишите /help")
        else:
            bot.send_message(message.chat.id, "Такой группы нет в расписании")


@bot.message_handler(commands=['remove_user'])
def remove_user(message: str):

    s = session()

    UserGroup = s.query(Groups).filter(Groups.TelegramID == message.chat.id).all()
    if len(UserGroup)>0:
        s.query(Groups).filter(Groups.TelegramID == message.chat.id).delete()
        bot.send_message(message.chat.id, "Вы отписались от рассылки группы " + UserGroup[0].GroupID)
        s.commit()
    else:
        bot.send_message(message.chat.id, 'Вы не подписаны ни на одну рассылку!')


@bot.message_handler(commands=['help'])
def help(message: str):
    
    bot.send_message(message.chat.id, "/add_user XXXXX - подписаться на рассылку группы XXXXX. Можно быть подписанным только на одну группу"
                                      "\n/remove_user - отписаться от текущей рассылки"
                                      "\n/getTimetable - получить список всех запланнированных конференций и их ссылок для своей группы" )


@bot.message_handler(commands=['info'])
def info(message: str):
    bot.send_message(message.chat.id,
                     "Данный бот был разработан для оптимизации учебного процесса. "
                     "Он предназначен для рассылки ссылок на предстоящие конференции в ZOOM для каждого студента")




@bot.message_handler(commands=['getTimetable'])
def getTimetable(message: str):
    s = session()

    userGroup = s.query(Groups).filter(Groups.TelegramID == message.chat.id).all()
    

    userTimetable = s.query(Timetable).filter(Timetable.GroupID == userGroup[0].GroupID).all()
    
    
    ans = ''
    for item in userTimetable:
        dtStringList = re.split(' |,|-|:', item.Time)
        dtList = list(map(str, dtStringList))

        lessonDT = dtList[2]+'.'+dtList[1]+' '+dtList[3]+':'+dtList[4]
        ans += lessonDT +' ' + str(item.Subject) + ' ' + str(item.ZoomLink)
        ans += '\n'
    #print(ans)
    if ans == '':
        bot.send_message(message.chat.id, "Для вашей группы нет расписания")
    else:    
        bot.send_message(message.chat.id, ans)
    
if __name__ == '__main__':
    bot.polling()
 
    

        

