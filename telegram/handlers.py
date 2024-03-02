#''' In this script, you have a function handle_new_messages that 
# takes an event and a session as parameters. This function is most 
# likely used as a callback for incoming telegram messages. The message 
# is then processed and input into a new TelegramMessage object before 
# being added to the session and committed to the database. If something 
# goes wrong during this process, an exception is caught and the error 
# is printed to the console. '''


# telegram/handlers. py
# Import the model for Telegram messages from db.models
from db.models import TelegramMessage

# Define async function to handle new incoming messages
async def handle_new_messages(event, session):
  try:   
    # Obtain message from event  
    message = event.message

    # Creating new instance of TelegramMessage with details from the new message
    new_message = TelegramMessage(
      chat_id=message.chat_id,  # chat id from obtained message
      text=message.text         # text from obtained message
    )

    # Add new instance of TelegramMessage to the session for commit
    session.add(new_message)

    # Commit the new message record in the database
    await session.commit()

    # Print a success message with chat id of saved message
    print(f'Saved new message from chat {message.chat_id}') 
  except Exception as e:  # If any error occurs during the process
      # Print an error message showing what went wrong
      print(f"Error saving message: {e}")