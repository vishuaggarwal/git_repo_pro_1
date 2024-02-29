# main.py

from telegram.filters import filter_messages
import asyncio
from telethon import events
from db.models import Session, engine, Base 
from telegram.client import init_telegram_client, client
from telegram.handlers import handle_new_messages
from datetime import datetime, timedelta
from db.models import Message
from telethon.tl.types import PeerChannel
from telegram.scraper import sc
from telegram.processor import process_messages
from telegram.scraper import scrape_channel

CHANNEL_IDS = [-100123, -100456, -100789]

def is_first_run(session):
  return session.query(Message).count() == 0

async def scrape_all_channels():
  scraping_tasks = []

  for channel_id in CHANNEL_IDS:
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

    for channel_id in CHANNEL_IDS:
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

async def save_message(msg, session):

  if msg.id not in get_existing_ids(session): 
    print('Saving new message...')
    session.add(Message(id=msg.id, text=msg.text))
    await session.commit()

# Import modules
from db import Session, engine, Base
from telegram.client import client
