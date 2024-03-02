# This code is essentially processing and storing Telegram 
# messages continuously. It first checks if it's the first run, and 
# if so it fetches the initial set of messages from the Telegram channels. 
# Then it continues to process incoming messages in real-time.

################################################################

# main.py
# Import necessary modules
import argparse
import asyncio
from datetime  import datetime, timedelta
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from telethon import events
# Import User defined module
from db.models import Base, TelegramChannel, TelegramMessage as Message
from telegram.client import init_telegram_client
from telegram.handlers import handle_new_messages
from telegram.scraper import scrape_channel, scrape_history
from telegram.processor import process_messages, process_historical
from telegram.filters import filter_messages
from db.models import Database

# Get the instance of Database
database = Database()

# Function to check first run by checking stored messages in database
async def is_first_run(Session):
    # Begin a new session
    async with Session() as session:
        async with session.begin():
            # Check if any stored message exists
            result = await session.execute(select(Message))
            # Get the result
            result = result.scalars().first()   # Don't use await here
            # If no stored message found then it's a first run
            return result is None

# The main function
async def main():
    # Initialize telegram client
    client = await init_telegram_client()
    # Create database session
    Session = sessionmaker(database.engine, expire_on_commit=False, class_=AsyncSession)
    async with Session() as session:
        async with session.begin():
            # Check if it is first run or not
            if await is_first_run(Session):
                # If first run then get message from the provided channels
                channel_ids = []
                for channel_id in channel_ids:
                    try:
                        messages = await client.get_messages(channel_id)                        
                    except Exception as e:
                        # Handle exceptions
                        messages = None
                        print(e)

                # For first run get last 30 days messages of a particular channel
                start = datetime.now() - timedelta(days=30)
                try:
                    # Try to scrape messages from last 30 days
                    messages = await client.get_messages('pythonchat', min_date=start)
                except Exception as e:
                    messages = None
                    print(e)
        
                # Filtering messages
                try:
                    filtered = filter_messages(messages) if messages else None
                except Exception as e:
                    filtered = None
                    print(e)

                # Save filtered messages to DB
                try:
                    if filtered:
                        for msg in filtered:
                            # Function to save messages in DB
                            await save_message(msg, Session)
                except Exception as e:
                    print(e)

            # Event-based processing for new incoming messages
            @client.on(events.NewMessage)
            async def handler(event):
                # On each new message event filter message and save new messages
                try:
                    filtered_new_messages = filter_messages([event.message])
                    if filtered_new_messages:
                        await save_message(filtered_new_messages[0], Session)
                except Exception as e:
                    print(e)

    # Start client and print a success message if started
    await client.start()
    print(' Program have been Started!')
    # Wait until the client disconnects
    await client.run_until_disconnected()

# Function to save messages in DB
async def save_message(msg, Session):
    if msg.id not in []:
        print('Saving new message...')
        try:
            async with Session() as session:
                async with session.begin():
                    # Insert new message in DB
                    session.add(Message(id=msg.id, text=msg.text))
        except Exception as e:
            print(e)

# Point to start the script
if __name__ == "__main__":
    # Parse command line arguments for initial data scraping
    parser = argparse.ArgumentParser()
    parser.add_argument("--initial_scrape", action="store_true", help="Perform an initial scrape of historical data.")
    parser.add_argument("--start_date", type=str, help="The start date for the historical scrape.")
    parser.add_argument("--end_date", type=str, help="The end date for the historical scrape.")
    args = parser.parse_args()
    start_date = args.start_date
    end_date = args.end_date

    # The main async function
    async def run():
        # Create the 'engine' of the DB
        await database.create_engine()
        # Create tables from the defined Database model 
        await database.create_tables()
        # Create database session
        Session = sessionmaker(database.engine, expire_on_commit=False, class_=AsyncSession)
        
        # If it's a initial run then scrape and save all historical data
        if args.initial_scrape:
            for batch in scrape_history(start_date, end_date):
                new_msgs = []
                for msg in process_historical(batch):
                    new_msgs.append(msg)
                async with Session() as session:
                    async with session.begin():
                        session.bulk_insert(new_msgs)

        # On normal run just call 'main' function
        await main()

    # Start the script in the event loop
    asyncio.run(run())