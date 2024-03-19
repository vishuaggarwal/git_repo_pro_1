# This Python script focuses on scraping messages from specific 
# Telegram channels. The channels are identified by their 
# IDs (CHANNEL_IDS). Messages within a certain date range can be gathered 
# using the scrape_history() function. The scraping for each channel 
# is done asynchronously using the scrape_channel() function and 
# multiple channels can be scraped simultaneously using asyncio.gather(). 
# Exception handling mechanisms have been put into place in each function 
# to manage any errors during the scraping process. 

# telegram/scraper.py
# Import process_messages from telegram.processor
import traceback
import re
import datetime

async def scrape_history(client, channel_id, offset_date):
    messages = []

    try:
        print('DEBUG: Scraping without offset_id')
        async for message in client.iter_messages(channel_id, offset_date=offset_date):
            msg_dict = {
                "id": message.id,
                "text": message.text,
                "chat_id": message.chat_id,
                "date": message.date
            }
            messages.append(msg_dict)

    except Exception as e:
        print(f"DEBUG: Error scraping history {channel_id}: {e}")
        traceback.print_exc()

    return messages