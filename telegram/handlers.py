# telegram/handlers. py

from db.models import TelegramMessage

async def handle_new_messages(event, session):

  try:    
    message = event .message

    new_message = TelegramMessage(
      chat_id=message.chat_id,
      text=message.text
    )

    session.add(new_message)
    await session.commit()

    print(f'Saved new message from chat {message. chat_id}')
  
  except Exception as e:
      print(f"Error saving message: {e}")
