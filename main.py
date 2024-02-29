# main.py

from telegram.filters import filter_messages
import asyncio, sqlalchemy, argparse
from telethon import events
from db.models import Session, engine, Base, TelegramChannel, TelegramMessage as Message
from telegram.client import init_telegram_client
from telegram.handlers import handle_new_messages
from datetime import datetime, timedelta
from telegram.scraper import scrape_channel, scrape_history
from telegram.processor import process_messages, process_historical
from config import create_engine, db_uri
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
session = Session()


def is_first_run(session):
  return session.query(Message).count() == 0   

#############################################################


parser = argparse.ArgumentParser()
parser.add_argument("--initial_scrape", action="store_true",help="Perform an initial scrape of historical data.")
parser.add_argument("--start_date", type=str,help="The start date for the historical scrape.")
parser.add_argument("--end_date", type=str,help="The end date for the historical scrape.")

args = parser.parse_args()
start_date = args.start_date
end_date = args.end_date

if args.initial_scrape:
   for batch in  scrape_history(start_date, end_date):
      new_msgs = []
      for msg in process_historical(batch):
         new_msgs.append(msg)
      session.bulk_insert(new_msgs) 


##############################################################
         
async def scrape_all_channels():
  channel_ids = []
  
  channels = TelegramChannel.query.all()

  for channel in channels:
    channel_ids.append(channel.id)
  
  scraping_tasks = []

  for channel_id in channel_ids:
    task = asyncio.create_task(scrape_channel(channel_id))
    scraping_tasks.append(task)

  await asyncio.gather(*scraping_tasks)

  @client.on(events.NewMessage)   
  async def handler(event):
    await scrape_all_channels()
  


async def main():

  session = Session()
  Base.metadata.create_all(engine)

  if is_first_run(session):

    channel_ids = []
    for channel_id in channel_ids:
      messages = await client.get_messages(channel_id)
      await process_messages(messages, session)

  @client.on(events.NewMessage)
  async def handler(event):
    await process_messages([event.message], session)
    
    # Get last 30 days of messages
    start = datetime.now() - timedelta(days=30)    
    messages = await client.get_messages('pythonchat', min_date=start)

    # Filter messages
    filtered = filter_messages(messages)

    # Save filtered messages
    for msg in filtered:
      await save_message(msg, session)

  @client.on(events.NewMessage)     
  async def handler(event):
    # Filter new message
    filtered = filter_messages([event.message])    
    if filtered:
      await save_message(filtered[0], session)

  await client.start()
  print('Started!')

  await client.run_until_disconnected()
  client = await init_telegram_client()

async def save_message(msg, session):
  if msg.id not in []:
    print('Saving new message...')   
    session.add(Message(id=msg.id, text=msg.text))
    await session.commit()


