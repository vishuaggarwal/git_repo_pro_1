from datetime import datetime
from dateutil.relativedelta import relativedelta
import asyncio

async def move_to_history(Session):
    async with Session() as session:
        async with session.begin():
            await session.execute("INSERT INTO TelegramMessagesHistory SELECT * FROM TelegramMessages")
            await session.execute("DELETE FROM TelegramMessages")
            await session.execute("INSERT INTO TelegramSentimentMessagesHistory SELECT * FROM TelegramSentimentMessages")
            await session.execute("DELETE FROM TelegramSentimentMessages")
            await session.commit()

async def rename_history(Session):
    async with Session() as session:
        async with session.begin():
            last_month = (datetime.now() - relativedelta(months=1)).strftime('%B_%Y')
            await session.execute(f"ALTER TABLE TelegramMessagesHistory RENAME TO TelegramMessagesHistory_{last_month}")
            await session.execute("CREATE TABLE TelegramMessagesHistory (LIKE TelegramMessages INCLUDING DEFAULTS INCLUDING GENERATED)")
            await session.execute(f"ALTER TABLE TelegramSentimentMessagesHistory RENAME TO TelegramSentimentMessagesHistory_{last_month}")
            await session.execute("CREATE TABLE TelegramSentimentMessagesHistory (LIKE TelegramSentimentMessages INCLUDING DEFAULTS INCLUDING GENERATED)")
            await session.commit()

            
async def daily_tasks(Session):
    current_day = datetime.now().day
    current_hour = datetime.now().hour

    while True:
        if datetime.now().day != current_day:  # a new day starts
            current_day = datetime.now().day
            await move_to_history(Session)  # move records from TelegramMessages to TelegramMessagesHistory

        if datetime.now().day == 1 and datetime.now().hour != current_hour:  # a new month begins in the first hour
            current_hour = datetime.now().hour
            await rename_history(Session)  # rename history table with last month's name

        await asyncio.sleep(3600)  # check every hour