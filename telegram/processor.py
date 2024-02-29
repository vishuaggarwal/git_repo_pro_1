from telegram.filters import filter_messages
from db import session
from db.models import Message

def process_historical(messages):
   for msg in messages:
      if msg.date < min_id or msg.id not in message_ids:
         yield msg
def is_new(msg, session):

  return msg.id not in {m.id for m in session.query(Message.id)}

async def process_messages(messages, session):

  filtered = filter_messages(messages)

  for msg in filtered:
     await save_message(msg, session)

async def save_message(msg, session):

  if is_new(msg, session):  
    new = Message(id=msg.id, text=msg.text)
    session.add(new)
    await session.commit()

