import requests
import config
import telebot
import datetime as DT 
import time
import re
from bs4 import BeautifulSoup
from typing import List, Tuple
from DB import Groups, Timetable, session

bot = telebot.TeleBot(config.access_token)
AllGroups = ['K3241', 'M3208']



if __name__ == '__main__':
    while True:
        s = session()
        now = DT.datetime.now()
        rows = s.query(Timetable).all()
        for row in rows:
            dtStringList = re.split(' |,|-|:', row.Time)
            dtList= list(map(int, dtStringList))
            
            lessonDT = DT.datetime(dtList[0],dtList[1],dtList[2],dtList[3],dtList[4],dtList[5])
            deltaTime = lessonDT - now
            if (deltaTime.seconds < 600):
                StudentList = s.query(Groups).filter(Groups.GroupID == row.GroupID).all()
                LessonTime = dtStringList[3]+":"+dtStringList[4]
                
                for student in StudentList:
                    bot.send_message(student.TelegramID, "Уведомляем вас о предстоящем занятии по предмету {} в {}. Ссылка на конференцию Zoom: {}".format(row.Subject, LessonTime, row.ZoomLink))
            
      
        time.sleep(302)

        
