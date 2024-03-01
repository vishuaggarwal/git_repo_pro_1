from filters import filter_messages
from db.models import TelegramMessage as Message

min_id = 0  # Initialize this with your value

def process_historical(messages):
    for msg in messages:
        if msg.date < min_id:  # Compare with actual value
            yield msg

async def is_new(msg, session):
    return not await session.query(Message.id).filter(Message.id == msg.id).first()

async def process_messages(messages, session):
    try:
        filtered = filter_messages(messages)
        for msg in filtered:
            await save_message(msg, session)
    except Exception as e:
        print(e)

async def save_message(msg, session):
    try:
        if await is_new(msg, session):
            new = Message(id=msg.id, text=msg.text)
            session.add(new)
            await session.commit()
    except Exception as e:
        print(f'error saving message: {e}')