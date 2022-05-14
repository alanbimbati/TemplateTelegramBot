from turtle import back
from xml.sax.handler import property_interning_dict
from telebot import types
from telebot import TeleBot
from telebot import util
from settings import *
import schedule
import time
bot = TeleBot(BOT_TOKEN, threaded=False)

def backup():
    doc = open('points.db', 'rb')
    bot.send_document(CHANNEL_LOG, doc, caption=PROJECT_NAME+"#database #backup")
    doc.close()

if BACKUP_DAILY:
    schedule.every().day.at("09:00").do(backup)

if BACKUP_HOURLY:
    schedule.every().hour.do(backup)

while True:
    schedule.run_pending()
    time.sleep(1)