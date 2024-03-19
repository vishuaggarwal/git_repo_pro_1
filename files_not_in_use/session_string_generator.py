# In the script, you start by importing necessary modules, then you attempt to 
# import Telethon and python-dotenv libraries which are essential for the script to run. 
# If these libraries are not present, the script exits. You then load environment variables, and 
# define a function to read these environment variables or user's input as required. Next, 
# you get the phone number from the user, and use it along with previously 
# read variables to log in to a telegram session. After that you display the session string 
# to console so the user can backup it for future use. You remind the user to keep the session 
# string in a secure place because it can be used to issue commands to the Telegram account 
# associated with it. Finally, you provide some links to help the user understand sessions better 
# and deactivate the session if it gets compromised.



# Import os for interaction with the OS
import os
# Import sys to interact with the Python interpreter
import sys

# Try to import necessary parts of Telethon
try:
    # TelegramClient is the main class of Telethon library
    from telethon.sync import TelegramClient
    # StringSession class allows you to save a session and export as a string
    from telethon.sessions import StringSession
except Exception as err:
    # Print the exception if importing Telethon failed
    print(err)
    print('\nFailed to import. Please install Telethon.\nRun\n\tpip install telethon')
    # Exit the script because Telethon is necessary for running the script
    sys.exit()

# Try to import dotenv for loading environment variables from .env file
try:
    from dotenv import load_dotenv
except Exception as err:
    # Print this note if importing dotenv failed
    print('Note: Could not load `.env` file, because python-dotenv package not present.')
    # Exit the script because dotenv is necessary for running the script
    sys.exit()
else:
    load_dotenv()

# Function to get value of a variable from environment or user input
def get_value(of_what: str):
    # Get the environment variable value
    val = os.getenv(of_what)
    # If no environment variable found, get user input
    if not val:
        val = input(f'Enter the value of {of_what}:\n>')
        # If no user input received, exit the script
        if not val:
            print('Received no input. Quitting.')
            sys.exit()
        # Return the user input value
        return val
    # Return the environment variable value
    return val


print('\nYou are now going to login, and the session string will be displayed on screen. \nYou need to copy that for future use.')

# A pause for the user to understand what to do next
input('\nPress [ENTER] to proceed \n?')

# Ask for the user's phone number
phone = input('Enter your phone number in international format: ')

# If no phone number was provided, end the script
if not phone:
    print('You did not enter your phone number. Quitting.')
    sys.exit()

# Start the Telegram client with the phone number provided
with TelegramClient(StringSession(), get_value('20254122'), get_value('b966c845c8ba8fb3b7f5d812c51ec832')).start(phone=phone) as client:
    print('\n\nBelow is your session string ⬇️\n\n')
    # Print the session string to save it for the user
    print(client.session.save())
    print('\nAbove is your session string ⬆️\n\n')

# Closing note for the user, reminding them to keep the session string safe
print('''
- Keep this string safe! Dont leak it.
- Anyone with this string can use it to login into your account and do anything they want to to do.
- For more information about Telethon Session Strings
\thttps://docs.telethon.dev/en/latest/concepts/sessions.html#string-sessions
- You can deactivate this session by going to your
\tTelegram App -> Settings -> Devices -> Active sessions
''')