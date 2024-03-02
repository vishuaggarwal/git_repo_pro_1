import asyncio
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import TelegramMessage as Message
from db.models import Database
from telegram.processor import process_messages, process_historical

database = Database()

async def main():
    try:
        # Create an engine and session for the database
        async with database.Session() as session:
            # Get the minimum ID of the messages that have been processed
            min_id = session.query(Message.id).order_by(Message.id).first()
            if min_id is not None: # Assuming you need min_id for process_historical
                messages = process_historical(min_id)
                # Check if the messages are not None or empty
                if messages: 
                    await process_messages(messages, session)
            
            # Committing the changes in with block
            await session.commit()
    except Exception as e: 
        print(f"Error occurred while processing messages: {e}")

if __name__ == "__main__":
    asyncio.run(main())