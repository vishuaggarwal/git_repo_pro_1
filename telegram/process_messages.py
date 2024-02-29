import asyncio
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession
from  db.models import Message
from telegram.processor import process_messages, process_historical

async def main():
     # Create an engine and session for the database
    engine = create_engine("mysql+asyncmy://user: password@host:port/database")
    Session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession) 
    async with Session() as session:
         # Get the minimum ID of the messages that have already been processed
        min_id = session.query(Message.id).order_by(Message.id).first()

        # Process the historical messages
        messages = process_historical(messages)
        await process_messages(messages,  session)

    # Commit the changes to the database
    await session.commit()

if __name__ == "__main__":
    asyncio.run(main())
