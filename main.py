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

def getChatid(message):
   chatid = 0
   if message.chat.type == "group" or message.chat.type == "supergroup":
      chatid = message.from_user.id
   elif message.chat.type == 'private':
      chatid = message.chat.id
   return chatid

def welcome(message):
   bot.reply_to(message,"Welcome!",reply_markup=hideBoard)

@bot.message_handler(commands=['start'])
def start(message):
   print(message.text)

@bot.message_handler(commands=['newAdmin'])
def newAdmin(message):
   print("newAdmin")
   utility = Utilities()
   # /newAdmin @username
   tokenized = message.text.split()
   if len(tokenized)>1:
      username = tokenized[1]
      user = utility.getUser(username)
      if user is None:
         bot.reply_to(message, "I don't know this user")
      else:
         if utility.addAdmin(user):
            bot.reply_to(message,username+" is now an admin of the bot!",reply_markup=hideBoard)
   else:
      bot.reply_to(message,"To add an admin type '/newAdmin @username'",reply_markup=hideBoard)


@bot.message_handler(content_types=util.content_type_media)
def any(message):
   print("any")
   utility = Utilities()
   if utility.CreateUserIfNotExist(message):
      welcome(message)
   
   chatid = getChatid(message)
   user = utility.getUser(chatid)
   command = message.text
   if utility.isAdmin(user):
      if command.startswith('/newAdmin'):
         newAdmin(message)

bot.infinity_polling()

