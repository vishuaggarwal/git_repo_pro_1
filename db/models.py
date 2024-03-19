# db/models.py


# This code describes the Database models for Telegram messages 
# and channels. It also sets up a Database class for creating and 
# handling connections and tables in the database.
######################################################################

# Import necessary modules for database operations
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, BigInteger, Float
from sqlalchemy.orm import scoped_session, relationship, sessionmaker, declarative_base
# Import aiomysql's sqlalchemy engine, asynccontextmanager, and sqlalchemy's asyncio extension
from aiomysql.sa import create_engine as create_sqlalchemy_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# Additional import aiomysql for database operations
from datetime import datetime

# Define a Database class to handle database connections and operations
class Database:
    def __init__(self):
        # Initial Setup for Session and Engine
        self._Session = None
        self.engine = None

    async def create_engine(self):
        # Method to establish async connection to your MySQL server
        self.engine = create_async_engine(
            "mysql+aiomysql://root@localhost/test",
            echo=True,
        )

    async def create_tables(self):
        # Asynchronous context manager function to create tables in the database
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    @property
    def Session(self):
        # Getter function for the Database Session
        if self._Session is None:
            self._Session = sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)
        return self._Session

# Initializing an instance of Database class
database = Database()

async def init_db():
    # Initialize the database
    await database.create_engine()
    # Create database tables
    await database.create_tables()
    # Return a database session for ORM operations
    return database.Session

# Creating Base model which offers essential ORM functionality
Base = declarative_base()

class TelegramChannel(Base):
    __tablename__ = 'telegram_channels'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    chnl_id = Column(BigInteger, unique=True)  # Making the `chnl_id` unique
    chnl_type = Column(String(255))
    messages = relationship("TelegramMessage", back_populates="channel") 
    sentiment_messages = relationship("TelegramSentimentMessage", back_populates="channel")

class TelegramMessage(Base):
    __tablename__ = 'telegram_messages'
    id = Column(Integer, primary_key=True)
    msg_id = Column(Float)
    ent_1 = Column(Float)
    ent_2 = Column(Float)
    ent_3 = Column(Float)
    tar_1 = Column(Float)
    tar_2 = Column(Float)
    tar_3 = Column(Float)
    tar_4 = Column(Float)
    tar_5 = Column(Float)
    tar_6 = Column(Float)
    tar_7 = Column(Float)
    tar_8 = Column(Float)
    tar_9 = Column(Float)
    stop = Column(Float)
    lev_val = Column(String(255))
    lev_type = Column(String(255))
    pos_type = Column(String(255))
    ticker = Column(String(255))
    chnl_id = Column(BigInteger, ForeignKey('telegram_channels.chnl_id'))  # Creating foreign key with `chnl_id`
    msg_date = Column(DateTime, default=datetime.utcnow)
    channel = relationship("TelegramChannel", back_populates="messages")
class TelegramSentimentMessage(Base):
    __tablename__ = 'telegram_sentiment_messages'
    id = Column(Integer, primary_key=True, autoincrement=True)
    msg_id = Column(Float)
    message = Column(String(255))
    msg_date = Column(DateTime, default=datetime.utcnow)
    chnl_id = Column(BigInteger, ForeignKey('telegram_channels.chnl_id'))  # Creating foreign key with `chnl_id`
    channel = relationship("TelegramChannel", back_populates="sentiment_messages")

############################## Previous Message Histoy Tables ##############################

class TelegramMessageHistory(Base):
    __tablename__ = 'telegram_messages_history'
    id = Column(Integer, primary_key=True)
    msg_id = Column(Float)
    ent_1 = Column(Float)
    ent_2 = Column(Float)
    ent_3 = Column(Float)
    tar_1 = Column(Float)
    tar_2 = Column(Float)
    tar_3 = Column(Float)
    tar_4 = Column(Float)
    tar_5 = Column(Float)
    tar_6 = Column(Float)
    tar_7 = Column(Float)
    tar_8 = Column(Float)
    tar_9 = Column(Float)
    stop = Column(Float)
    lev_val = Column(String(255))
    lev_type = Column(String(255))
    pos_type = Column(String(255))
    ticker = Column(String(255))
    chnl_id = Column(BigInteger) 
    msg_date = Column(DateTime, default=datetime.utcnow)

class TelegramSentimentMessageHistory(Base):
    __tablename__ = 'telegram_sentiment_messages_history'
    id = Column(Integer, primary_key=True, autoincrement=True)
    msg_id = Column(Float)
    message = Column(String(255))
    msg_date = Column(DateTime, default=datetime.utcnow)
    chnl_id = Column(BigInteger)  
    
