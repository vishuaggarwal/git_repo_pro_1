# Telegram/client.py

# This code is initializing a Telegram client using the Telethon 
# library, and then it sets up a listener for new messages, which 
# it prints to the console. The API credentials and session key are 
# imported from a config file.

# Import necessary modules
import asyncio
import os
from getpass import getpass
from telethon import TelegramClient, events
from telethon.errors import SessionPasswordNeededError
from telethon.network import ConnectionTcpAbridged
from telethon.sessions import StringSession

# Import Telegram API credentials from the config file
from config import api_id, api_hash

# Import logger from log_config
from log_config import configure_logger

# Set up logging
init_logger = configure_logger('init_telegram_client', 'init_telegram_client.log')
main_logger = configure_logger('main_telegram_client', 'main_telegram_client.log')

async def init_telegram_client():
    session_file = 'session.txt'
    if os.path.exists(session_file):
        with open(session_file, 'r') as f:
            session_str = f.read()
        session = StringSession(session_str)
    else:
        session = StringSession()

    try:
        print('Initializing Telegram client...')
        client = TelegramClient(session, api_id, api_hash)
        await client.connect()

        if not client.is_connected():
            raise IOError("Failed to connect")

        if not await client.is_user_authorized():
            phone = input("Enter phone number: ")
            await client.send_code_request(phone)
            verification_code = input("Enter verification code: ")
            await client.sign_in(phone, verification_code)

        with open(session_file, 'w') as f:
            f.write(client.session.save())

        print('Telegram client initialized!')
        return client
    except SessionPasswordNeededError:
        await client.sign_in(password=getpass())
    except Exception as e:
        init_logger.error("Error in init_telegram_client function: ", exc_info=True)
        return None

async def main():
    while True:
        client = await init_telegram_client()

        if not client:
            print('Initialization failed. Retrying in 30 seconds...')
            await asyncio.sleep(30)
            continue

        @client.on(events.NewMessage)
        async def handle_new_message(event):
            try:
                print(f'New message: {event.raw_text}')
            except Exception as e:
                main_logger.error("Error in handle_new_message: ", exc_info=True)

        print('Client is running...')
        await client.run_until_disconnected()
        print('Client disconnected. Retrying in 30 seconds...')
        await asyncio.sleep(30)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


#action to take in future related to this script
    
    # Store the sessio_key in Database and load it through
    # dotenv