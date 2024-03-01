# db/models.py 

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
from aiomysql.sa import create_engine as create_sqlalchemy_engine
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import aiomysql

class Database:
    def __init__(self):
        self._Session = None
        self.engine = None

    async def create_engine(self):
        self.engine = create_async_engine(
            "mysql+aiomysql://root@localhost/test",
            echo=True,
        )

    async def create_tables(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    @property
    def Session(self):
        if self._Session is None:
            self._Session = sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)

        return self._Session

# Setup database
database = Database()

async def init_db():
    await database.create_engine()
    await database.create_tables()
    return database.Session

Base = declarative_base()

class TelegramMessage(Base):
    __tablename__ = 'telegram_messages'
    id = Column(Integer, primary_key=True)
    chat_id = Column(Integer) 
    message = Column(String(255))

class TelegramChannel(Base):
    __tablename__ = 'telegram_channels'
    id = Column(Integer, primary_key =True)
    name = Column(String(255))