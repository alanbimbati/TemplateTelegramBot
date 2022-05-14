from telebot import types
from telebot import TeleBot
from settings import *
from sqlalchemy         import create_engine
from sqlalchemy.orm     import sessionmaker

from model import Utente,Points, db_connect, create_table
import Points
from telebot import util

bot = TeleBot(BOT_TOKEN, threaded=False)


hideBoard = types.ReplyKeyboardRemove()  



@bot.message_handler(commands=['start'])
def start(message):
   pass
   

bot.infinity_polling()

