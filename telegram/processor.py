from telegram.filters import  filter_messages
from db.models import TelegramMessage as Message, Session
min_id = None

def process_historical(messages):
   for  msg in messages:
      if msg.date < min_id or msg.id not in Message.id:
         yield msg
def is_new(msg, session):
  return msg.id not in {m.id for m in session.query(Message.id)}

async def  process_messages(messages, session):
  try:
    filtered = filter_messages(messages)
    for msg in filtered:
       await save_message(msg, session)
  except Exception as e:
    print(e)

async def save_message(msg, session):

  try:
    if is_new(msg, session):  
      new = Message(id=msg. id, text=msg.text)
      session.add(new)
      await session.commit()
  except Exception as e:
    print(f'error saving message: {e}')


