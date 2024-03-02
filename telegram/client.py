# This code is initializing a Telegram client using the Telethon 
# library, and then it sets up a listener for new messages, which 
# it prints to the console. The API credentials and session key are 
# imported from a config file.


# Telegram/client.py

# Import necessary modules
import asyncio
import keyring
from telethon import TelegramClient, events
from telethon.sessions import StringSession
# Import Telegram API credentials from the config file
from config import api_id, api_hash, session_key

# Uncomment the following section if you are storing API credentials in a keyring.
# Retrieve API credentials from the keyring
# api_id = keyring.get_password('telegram', api_id)
# api_hash = keyring.get_password('telegram', api_hash)
# session_key = keyring.get_password('telegram', session_key)

# Print API credentials to check if they are correct
# print(f'your API ID is {api_id}')
# print(f'your API HASH is {api_hash}')

# Asynchronous function to initialize a Telegram client
async def init_telegram_client():
    # Create a new Telegram session
    session = StringSession(session_key)
    try:
        print('Initializing Telegram client...')
        # Initialize Telegram client with the provided session and API credentials
        client = TelegramClient(session, api_id, api_hash)
        # Connect to the Telegram server
        await client.connect()
        # Raise an error if failed to connect to the Telegram server
        if not client.is_connected():
            raise IOError("Failed to connect")
        # Start the Telegram client
        await client.start()
        print('Telegram client initialized!')
        # Return the initialized Telegram client
        return client
    except Exception as e:
        print(f'Telegram client initialization failed: {e}')
        # Return None when client initialization fails
        return None  

# Main asynchronous function
async def main():
    # Initialize Telegram client
    client = await init_telegram_client()
    # Stop the execution if client initialization failed
    if not client:
        print('Exiting due to failure in initialization of Telegram client')
        return
    # Add event handler for new incoming messages
    @client.on(events.NewMessage)
    async def handle_new_message(event):
        # Print the text of the new message
        print(f'New message: {event.raw_text}')
    # Start the client and run it until disconnected
    await client.run_until_disconnected()

# Main entry point of the script
if __name__ == '__main__':
    # Start the event loop
    loop = asyncio.get_event_loop()
    # Execute the main function until it is complete
    loop.run_until_complete(main())