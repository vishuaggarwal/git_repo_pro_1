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
from telegram.processor import process_messages

# Import init_telegram_client from telegram.client
from telegram.client import init_telegram_client

# Import asyncio for running tasks asynchronously
import asyncio

# Define asyncio scraper function to gather messages within a certain date range
async def  scrape_history(self, channel, start_date,  end_date):
    # Create empty list to hold messages
    messages = []

    try:
        # Iterate over pages of messages from the telegram channel 
        # limit by 100 messages per page, starting from the start date and reversing the order
        async for page in self.client.iter_messages(channel, offset_date=start_date, reverse=True, limit=100):
            # For each page, extend the list of messages with the messages from this page
            messages.extend(page.messages)
    except Exception as e:  # If any exception occurs while fetching messages
        # Print out the exception along with a descriptive error message
        print(f"Error scraping history {channel}: {e}")

    # Return the list of messages
    return messages

# Define asyncio function to scrape a channel
async def scrape_channel(client, channel_id):
    try:
        # Initialize the telegram client
        client = await init_telegram_client()
        # Get messages from the channel
        messages = await client.get_messages(channel_id)
        # Process the messages
        await process_messages(messages)
    except Exception as e:  # If any exception occurs while scraping the channel
        # Print out the exception along with a descriptive error message
        print(f"Error scraping channel {channel_id}: {e}")

# List of channel ids to scrape
CHANNEL_IDS = []

# Create a list of scraping tasks for each channel id
scraping_tasks = [scrape_channel(id) for id in CHANNEL_IDS]

# Define the main function to run the scraping tasks
async def main():
    try:
        # Use asyncio.gather to run all scraping tasks concurrently
        await asyncio.gather(*scraping_tasks)
    except Exception as e:  # If any exception occurs while running the scraping tasks
        # Print out the exception along with a descriptive error message
        print(f"Error running scraping tasks: {e}")