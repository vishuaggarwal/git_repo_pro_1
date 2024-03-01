### cron to this in linux "0 0 * * *  python /path/to/process_messages.py"

import asyncio
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from  sqlalchemy.ext.asyncio import AsyncSession
from db.models import TelegramMessage as Message
from db.models import Session
from telegram.processor import process_messages, process_historical

async def main():
    try:
        # Create an engine and session for the database
        async with Session() as session:
            # Get the minimum ID of the messages that have already been processed
            min_id = session.query(Message.id).order_by(Message.id).first()

            # Process the historical messages
            messages = process_historical(messages)
            await process_messages(messages, session)

        # Commit the changes to the database
        await session.commit()
    except Exception as e: 
        print(f"Error occurred while processing messages: {e}")

if __name__ == "__main__":
    asyncio.run(main())
