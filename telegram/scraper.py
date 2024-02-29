# telegram/scraper.py
from telegram.processor import process_messages
from telegram.client import init_telegram_client
import asyncio

async def  scrape_history(self, channel, start_date, end_date):
    messages = []
    async for page in self.client.iter_messages(channel, offset_date=start_date, reverse=True, limit=100):
        messages.extend(page.messages )
    return messages

async def scrape_channel(channel_id):
  messages = await client.get_messages(channel_id)
  await process_messages(messages)
  client = await init_telegram_client()

CHANNEL_IDS = []
scraping_tasks = [scrape_channel(id) for id in CHANNEL_IDS]
async def main():
    await asyncio.gather(*scraping_tasks)

    
    