import asyncio
import keyring
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from config import api_id, api_hash, session_key

#api_id = keyring.get_password('telegram', api_id)
#api_hash = keyring.get_password('telegram', api_hash)
#session_key = keyring.get_password('telegram', session_key)

print(f'your API ID is {api_id}')
print(f'your API HASH is {api_hash}')

async def init_telegram_client():
    session = StringSession(session_key)
    try:
        print('Initializing Telegram client...')
        client = TelegramClient(session, api_id, api_hash)
        await client.connect()
        if not client.is_connected():
            raise IOError("Failed to connect")
        await client.start()
        print('Telegram client initialized!')
        return client
    except Exception as e:
        print(f'Telegram client initialization failed: {e}')
        return None  # Return None when client initialization fails


async def main():
    client = await init_telegram_client()
    # Stop the execution if client initialization failed
    if not client:
        print('Exiting due to failure in initialization of Telegram client')
        return
    # Add event handlers here
    @client.on(events.NewMessage)
    async def handle_new_message(event):
        print(f'New message: {event.raw_text}')
    
    await client.run_until_disconnected()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())