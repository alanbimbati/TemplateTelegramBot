from telebot import types
from telebot import TeleBot
from settings import *
from sqlalchemy         import create_engine, true
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

@bot.message_handler(commands=['deleteMe'])
def deleteMe(message):
   msg = bot.reply_to(message, 'Are you sure to delete your account? then write `YES,I AM`',parse_mode='markdown')
   bot.register_next_step_handler(msg, Delete)
def Delete(message):
   utility = Utilities()
   if message.text=='YES,I AM':
      chatid = getChatid(message)
      utility.deleteAccount(chatid)
      bot.reply_to(message,'Your account is deleted')
   else:
      bot.reply_to(message, 'Good news! Your account still alive!')

@bot.message_handler(commands=['menu'])
def menu(message):
   utility = Utilities()
   father = None
   menu = utility.menu(father)
   markup = types.ReplyKeyboardMarkup()
   for item in menu:
      markup.add(item.command)

   msg = bot.reply_to(message,"Choose a command",reply_markup=markup)
   bot.register_next_step_handler(msg,subMenu)

@bot.message_handler(commands=['addCommand'])
def addCommand(message):
   utility = Utilities()
   chatid = getChatid(message)
   user = utility.getUser(chatid)
   tokenized = message.text.split()
   command = None
   father  = None
   if len(tokenized)>=2:
      # /addCommand comando father
      try:
         command = tokenized[1]
         father = tokenized[2]
      except:
         print('father does not exist, I create a command on root')
      if utility.isAdmin(user):
         utility.addCommand(command,father)
   else:
      bot.reply_to(message, "To add a command type _/addCommand command father_\n you can even type _/addCommand command_ withouth the father, the command will appear on the root menu",parse_mode='markdown')



def subMenu(message):
   print(message.text)
   utility = Utilities()
   father = message.text
   subMenu = utility.menu(father)
   markup = types.ReplyKeyboardMarkup()
   for item in subMenu:
      markup.add(item.command)
   msg = bot.reply_to(message,"Choose a command",reply_markup=markup)
   bot.register_next_step_handler(msg,subMenu)
   



# Any other messages
@bot.message_handler(content_types=util.content_type_media)
def any(message):
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

