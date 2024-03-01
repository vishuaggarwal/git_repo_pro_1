# main.py
import argparse
import asyncio
from datetime  import datetime, timedelta
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from telethon import events
from db.models import Base, TelegramChannel, TelegramMessage as Message
from telegram.client import init_telegram_client
from telegram.handlers import handle_new_messages
from telegram.scraper import scrape_channel, scrape_history
from telegram.processor import process_messages, process_historical
from telegram.filters import filter_messages
from db.models import Database


database = Database()

async def is_first_run(Session):
    async with Session() as session:
        async with session.begin():
            result = await session.execute(select(Message))
            result = result.scalars().first()   # Don't use await here
            return result is None
        

async def main():
    client = await init_telegram_client()
    Session = sessionmaker(database.engine, expire_on_commit=False, class_=AsyncSession)
    async with Session() as session:
        async with session.begin():
            if await is_first_run(Session):
                channel_ids = []
                for channel_id in channel_ids:
                    try:
                        messages = await client.get_messages(channel_id)                        
                    except Exception as e:
                        messages = None
                        print(e)

                # Get last 30 days of messages
                start = datetime.now() - timedelta(days=30)
                try:
                    # Remove min_date if it's not supported.
                    messages = await client.get_messages('pythonchat', min_date=start)
                except Exception as e:
                    messages = None
                    print(e)
        
                # Filter messages
                try:
                    filtered = filter_messages(messages) if messages else None
                except Exception as e:
                    filtered = None
                    print(e)
        
                # Save filtered messages
                try:
                    if filtered:
                        for msg in filtered:
                            await save_message(msg, Session)
                except Exception as e:
                    print(e)

            # Event-based processing
            @client.on(events.NewMessage)
            async def handler(event):
                # Filter new message
                try:
                    filtered_new_messages = filter_messages([event.message])
                    if filtered_new_messages:
                        await save_message(filtered_new_messages[0], Session)
                except Exception as e:
                    print(e)

    await client.start()
    print(' Program have been Started!')

    await client.run_until_disconnected()

async def save_message(msg, Session):
    if msg.id not in []:
        print('Saving new message...')
        try:
            async with Session() as session:
                async with session.begin():
                    session.add(Message(id=msg.id, text=msg.text))
        except Exception as e:
            print(e)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--initial_scrape", action="store_true", help="Perform an initial scrape of historical data.")
    parser.add_argument("--start_date", type=str, help="The start date for the historical scrape.")
    parser.add_argument("--end_date", type=str, help="The end date for the historical scrape.")
    args = parser.parse_args()
    start_date = args.start_date
    end_date = args.end_date

    async def run():
        await database.create_engine()
        await database.create_tables()
        Session = sessionmaker(database.engine, expire_on_commit=False, class_=AsyncSession)
        
        if args.initial_scrape:
            for batch in scrape_history(start_date, end_date):
                new_msgs = []
                for msg in process_historical(batch):
                    new_msgs.append(msg)
                async with Session() as session:
                    async with session.begin():
                        session.bulk_insert(new_msgs)

        await main()

    asyncio.run(run())