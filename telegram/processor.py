# From this script, it gets data from telegram messages performs a 
# check on the date of the messages using set value min_id, filter 
# the messages with the necessary conditions and persist in the database. 
# If a message is already in database, it is not persist again. 
# There is comprehensive error handling in place in case anything goes 
# wrong. It's an asynchronous code to ensure non-blocking execution.


# Telegram/processor.py
# Importing filter_messages function from telegram.filters
from telegram.filters import filter_messages

# Importing necessary Database models from db.models
from db.models import Base, TelegramChannel, TelegramMessage as Message

# Allocate a global variable min_id with an initial value, replace it with your value
min_id = 0  

# Function to process historical telegram messages
def process_historical(messages):
    # Loop through each message provided as input
    for msg in messages:
        # Check if the date of the message is less than min_id
        if msg.date < min_id:  # Replace with comparison with actual value
            # If true, yield this message for processing
            yield msg


# Asynchronous function to check if a message is new
async def is_new(msg, session):
    # Return True if the message id is not in the database, False otherwise
    return not await session.query(Message.id).filter(Message.id == msg.id).first()


# Asynchronous function to process messages
async def process_messages(messages, session):
    try:
        # Filter provided messages
        filtered = filter_messages(messages)
        # Loop through each filtered message
        for msg in filtered:
            # Save each message using the session
            await save_message(msg, session)
    # If any exception occurs, print the exception
    except Exception as e:
        print(e)


# Asynchronous function to save a message
async def save_message(msg, session):
    try:
        # Check if the message is new
        if await is_new(msg, session):
            # If the message is new, prepare to save it to the database
            new = Message(id=msg.id, message=msg.text)
            # Add the new message to the database session
            session.add(new)
            # Commit the session to save the message in the database
            await session.commit()
    # If any exception occurs, print the exception along with a descriptive error message
    except Exception as e:
        print(f'error saving message: {e}')