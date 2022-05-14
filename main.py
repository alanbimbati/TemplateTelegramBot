from telebot import types
from telebot import TeleBot
from settings import *
from sqlalchemy         import create_engine
from sqlalchemy.orm     import sessionmaker

from model import User, db_connect, create_table
from telebot import util
from Utilities import Utilities
bot = TeleBot(BOT_TOKEN, threaded=False)


hideBoard = types.ReplyKeyboardRemove()  


@bot.message_handler(commands=['start'])
def start(message):
   pass

def welcome(message):
   bot.reply_to(message,"Welcome!")

@bot.message_handler(content_types=util.content_type_media)
def any(message):

   if message.chat.type == "group" or message.chat.type == "supergroup":
      chatid = message.from_user.id
   elif message.chat.type == 'private':
      chatid = message.chat.id

   utility = Utilities()
   if utility.CreateUser(message):
      welcome(message)
   

bot.infinity_polling()

