from telebot import TeleBot
from telebot import types

from sqlalchemy.sql import functions
from sqlalchemy         import create_engine, null
from sqlalchemy         import update
from sqlalchemy         import desc
from sqlalchemy.orm     import sessionmaker
from model import User,Menu, db_connect, create_table

from settings import *

class Utilities:    
    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def CreateUserIfNotExist(self, message):
        session = self.Session()
        if message.chat.type == "group" or message.chat.type == "supergroup":
            info = message.from_user
        elif message.chat.type == 'private':
            info = message.chat
        chatid = info.id
        username = '@'+info.username
        name = info.first_name
        last_name = info.last_name

        exist = session.query(User).filter_by(id_telegram = chatid).first()
        firstUser = len(session.query(User).all())==0

        if exist is None:
            try:
                user = User()
                user.username     = username
                user.name         = name
                user.id_telegram  = chatid
                user.last_name      = last_name
                if firstUser:
                    user.admin=1
                else:
                    user.admin  = 0
                session.add(user)
                session.commit()
            except:
                session.rollback()
                raise
            finally:
                session.close()
            return True
        elif exist.username!=username:
            self.update_user(chatid,{'username':username})
        return False

    def getUser(self, target):
        session = self.Session()
        utente = None
        target = str(target)
        if target.startswith('@'):
            utente = session.query(User).filter_by(username = target).first()
        elif target.isdigit():
            chatid = int(target)
            utente = session.query(User).filter_by(id_telegram = chatid).first()
        return utente


    def update_user(self, chatid, kwargs):
        session = self.Session()
        utente =  session.query(User).filter_by(id_telegram=chatid).first()
        for key, value in kwargs.items():  # `kwargs.iteritems()` in Python
            print("updating ",key, "in ",value)
            setattr(utente, key, value) 
        session.commit()
        session.close()

        
    def deleteAccount(self,chatid):
        session = self.Session()
        utente = session.query(User).filter_by(id_telegram = chatid).first()  
        session.delete(utente)
        session.commit()


    def getUsernameAtLeastName(self,utente):
        nome = ''
        if utente.username is None:
            nome = utente.nome
        else:
            nome = utente.username
        return nome

    def addAdmin(self,utente):
        session = self.Session()
        if utente is None:
            return False     
        exist = session.query(User).filter_by(id_telegram = utente.id_telegram,admin=1).first()
        if exist is None:
            user = session.query(User).filter_by(id_telegram = utente.id_telegram).first()
            if user is not None:
                self.update_user(user.id_telegram,{'admin':1})
                return True
        else:
            return False

    def isAdmin(self,utente):
        session = self.Session()
        exist = session.query(User).filter_by(id_telegram = utente.id_telegram,admin=1).first()
        if exist is not None:
            return True
        else:
            return False

    def menu(self,father):
        session = self.Session()
        menu = session.query(Menu).filter_by(father = father).all()
        return menu

    def addCommand(self,command,father):
        session = self.Session()    
        exist = session.query(Menu).filter_by(command = command,father=father).first()
        if exist is None:  
            try:
                menu = Menu()
                menu.command = command
                menu.father  = father
                session.add(menu)
                session.commit()
            except:
                session.rollback()
                raise
            finally:
                session.close()
            return True
        else:
            return False
            