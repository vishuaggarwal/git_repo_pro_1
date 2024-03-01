# telegram/client.py

import asyncio
import keyring
from telethon import TelegramClient, events
from telethon.sessions import StringSession

api_id = keyring.get_password('telegram', 'api _id')
api_hash = keyring.get_password('telegram', 'api_hash')


async def init_telegram_client():
  session = StringSession('my_session')
  try:
    print('Initializing Telegram client...')
    client = TelegramClient(session, api_id, api_hash)
    await client.connect()
    await client.start()
    print('Telegram client initialized!')
  except Exception as e:
    print(f'Telegram client initialization failed: {e}')
  return client


async def main():
  client = await init_telegram_client()

  if client:
    # Add event handlers here
    @client.on(events.NewMessage)
    async def handle_new_message (event):
      print(f'New message: {event.raw_text}')
  
    await client. run_until_disconnected()

if __name__ == '__main__':
  
  loop = asyncio.get_event_loop()
  loop.run_until_complete(main())
