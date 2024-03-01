# db/models.py

import sqlalchemy
from sqlalchemy import  Column, Integer, String
import sqlalchemy.ext.declarative
from sqlalchemy.ext.declarative import declarative_base  
import sqlalchemy
from sqlalchemy  import Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine= create_engine("mysql+asyncmy://root@localhost:3306/test.db")
Session = sessionmaker(bind=engine )


Base = declarative_base()

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

  # Add error handling for SQLAlchemy operations
  try:
     Base.metadata.create_all(engine)
  except Exception as e:
    print(f"Error creating database tables: {e}")
