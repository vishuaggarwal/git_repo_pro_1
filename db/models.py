# db/models.py

import sqlalchemy
from sqlalchemy import Column, Integer, String
import sqlalchemy.ext.declarative
from sqlalchemy.ext.declarative import declarative_base  
from utils.db import Base
import sqlalchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

engine = sqlalchemy.create_engine('mysql+mysqlconnector://user:password@localhost/dbname')


class TelegramMessage(Base):
    __tablename__ = 'telegram_messages'
    
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer) 
    message = Column(String)

class TelegramChannel(Base):
  __tablename__ = 'telegram_channels'
  
  id = Column(Integer, primary_key=True)
  name = Column(String)
  # other columns like name, description etc