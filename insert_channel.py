# insert_channel.py

import asyncio
from termcolor import colored
from sqlalchemy import select
from db.models import TelegramChannel, init_db

async def add_channel():
    session_factory = await init_db()
    async with session_factory.begin() as session:
        while True:
            try:
                channel_id = int(input(colored('Enter the ID of the Telegram Channel: ', 'yellow')))
                stmt = select(TelegramChannel).where(TelegramChannel.chnl_id == channel_id)
                result = await session.execute(stmt)
                exist_channel = result.scalar_one_or_none()

                if exist_channel:
                    print(colored('Channel ID already exists in DB. Try again with different ID', 'red'))
                    continue

                channel_name = input(colored('Enter the Name of the Telegram Channel: ', 'yellow'))
                print(colored('Enter the Type of the Telegram Channel: ', 'yellow'))
                print(colored('Press 1 for Signal', 'green'))
                print(colored('Press 2 for Sentiment', 'green'))
                channel_type_option = input()
                channel_type = 'Signal' if channel_type_option == '1' else 'Sentiment' if channel_type_option == '2' else None

                if channel_type is None:
                    print(colored("Invalid channel type selected. Exiting.", 'red'))
                    return

                new_channel = TelegramChannel(
                    chnl_id=channel_id,
                    name=channel_name,
                    chnl_type=channel_type
                )

                session.add(new_channel)
                print(colored(f"Channel({channel_name} - {channel_id}) saved to Database. Success!", 'green'))
            except Exception as e:
                print(e)
                session.rollback()

            more_records = input(colored("Do you want to add more records? (y/n): ", 'yellow'))
            if more_records.lower() != 'y':
                break
    await session.commit()

if __name__ == "__main__":
    asyncio.run(add_channel())