# telegram/scraper.py
from telegram.processor import process_messages
from telegram.client import init_telegram_client
import asyncio

async def  scrape_history(self, channel, start_date,  end_date):
    messages = []
    try:
        async for page in self.client.iter_messages(channel, offset_date=start_date, reverse=True, limit=100):
            messages.extend(page.messages )
    except Exception as e: 
        print(f"Error scraping history {channel}: {e}")
    return messages

async def scrape_channel(client, channel_id):
    try:
        client = await init_telegram_client()
        messages = await client.get_messages(channel_id)
        await process_messages(messages)
    except Exception as e:
        print(f"Error scraping channel {channel_id}: {e}")

CHANNEL_IDS = []
scraping_tasks = [scrape_channel(id) for id in CHANNEL_IDS]
async def main():
    try:
        await asyncio.gather(*scraping_tasks )
    except Exception as e:
        print(f"Error running scraping tasks: {e}")

