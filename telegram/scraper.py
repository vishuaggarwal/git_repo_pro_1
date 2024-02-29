# telegram/scraper.py
from telegram.processor import process_messages
from telegram.client import client

async def scrape_channel(channel_id):
  messages = await client.get_messages(channel_id)
  await process_messages(messages) 

    scraping_tasks = [scrape_channel(id) for id in CHANNEL_IDS]
    await asyncio.gather(*scraping_tasks) 
