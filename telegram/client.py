# telegram/client.py

import asyncio
import keyring
from telethon import TelegramClient, events
from telethon.sessions import StringSession 

api_id = keyring.get_password('telegram', 'api_id')
api_hash = keyring.get_password('telegram', 'api_hash')

async def init_telegram_client():

  session = StringSession('my_session')

  print('Initializing Telegram client...')

  client = TelegramClient(session, api_id, api_hash)

  await client.start()

  print('Telegram client initialized!')

  return client


async def main():

  client = await init_telegram_client()

  # Add event handlers here

  await client.run_until_disconnected()


if __name__ == '__main__':
  
  loop = asyncio.get_event_loop()
  loop.run_until_complete(main())