from ast import Str
from datetime import date
from termios import TIOCPKT_FLUSHREAD
from sqlalchemy                 import create_engine, Column, Table, ForeignKey, MetaData
from sqlalchemy.orm             import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy                 import (Integer, String, Date, DateTime, Float, Boolean, Text)

Base = declarative_base()


def db_connect():
    return create_engine('sqlite:///points.db')
    
def create_table(engine):
    Base.metadata.create_all(engine)

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    id_telegram = Column('id_Telegram', Integer, unique=True)
    name  = Column('name', String(32))
    surname = Column('surname', String(32))
    username = Column('username', String(32), unique=True)
    admin = Column('admin',Boolean)