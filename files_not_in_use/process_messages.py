# The script processes Telegram messages, ideally stored in a database. 
# The smallest id of the processed messages is found and then passed 
# to the process_historical() function. The returned messages are then 
# processed. Note that the script is designed to run asynchronously, 
# with exception handling in case of errors during the process.

### Sets up a recurring task in Unix-like operating systems
### to execute the script every day at midnight
### Command: "0 0 * * *  python /path/to/process_messages.py"

# import necessary modules from built-in, third-party libraries
import asyncio
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession
# import custom built models and functions for handling telegram messages
from db.models import TelegramMessage as Message
from db.models import Database
from telegram.processor import process_messages, process_historical

# Instantiate the Database class 
database = Database()

# define the main function to be run asynchronously 
async def main():
    try:
        # initializing the database session
        async with database.Session() as session:
            # Get the first(ID is the smallest) processed message
            min_id = session.query(Message.id).order_by(Message.id).first()
            # if there are processed messages
            if min_id is not None: 
                # process and return messages based on min_id
                messages = process_historical(min_id)
                # if there are messages to be processed
                if messages: 
                    # process messages and use the session
                    await process_messages(messages, session)
            # commit the changes made within this context
            await session.commit()
    # if there occurred any exception
    except Exception as e: 
        # print out the Exception
        print(f"Error occurred while processing messages: {e}")

# if this file is run as a main file
if __name__ == "__main__":
    # start the event loop and run the main function
    asyncio.run(main())