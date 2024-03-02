# This code describes the Database models for Telegram messages 
# and channels. It also sets up a Database class for creating and 
# handling connections and tables in the database.
######################################################################
# db/models.py
# Import necessary modules for database operations
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
# Import aiomysql's sqlalchemy engine, asynccontextmanager, and sqlalchemy's asyncio extension
from aiomysql.sa import create_engine as create_sqlalchemy_engine
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
# Additional import aiomysql for database operations
import aiomysql

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

class TelegramMessage(Base):
    # Defining a model for Telegram messages
    # Name of the table as it appears in database
    __tablename__ = 'telegram_messages'
    # Declare Column(S) which are essentially fields in the database table;
    # each one is instance of Column and takes a type as its first argument, declares it as primary key
    id = Column(Integer, primary_key=True)
    # Chat id of the messages
    chat_id = Column(Integer) 
    # The actual message body
    message = Column(String(255))

class TelegramChannel(Base):
    # Define a model for Telegram channels
    __tablename__ = 'telegram_channels'
    # Channel ID set as primary key
    id = Column(Integer, primary_key=True)
    # Name of the channel
    name = Column(String(255))
    # Integer ID of the channel, not nullable and default value (-1)
    chnl_id = Column(Integer, nullable=False, default=-1)