# db/models.py

from sqlalchemy import Column, Integer, String 
from sqlalchemy.ext.declarative import declarative_base
from utils.db import Base

Base = declarative_base() 

class TelegramMessage(Base):
    __tablename__ = 'telegram_messages'
    
    id = Column(Integer, primary_key=True) 
    chat_id = Column(Integer)
    message = Column(String)
