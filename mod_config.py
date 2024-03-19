# config.py

# Import necessary modules
from dotenv import load_dotenv
from sqlalchemy import create_engine
import os

# Load the contents of the .env file
load_dotenv()

# Define database parameters
DATABASE_USERNAME = os.getenv('DATABASE_USERNAME')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_PORT = os.getenv('DATABASE_PORT')
DATABASE_NAME = os.getenv('DATABASE_NAME')

# Define the telegram API credentials
api_id = os.getenv('TELEGRAM_API_ID', "20254122")
api_hash = os.getenv('TELEGRAM_API_HASH', 'b966c845c8ba8fb3b7f5d812c51ec832')
session_key = os.getenv('TELEGRAM_SESSION_KEY', '1BVtsOJ0Buwbgwiopb6X3b-mO68dtQboJqg_icCTr21DtRsH5YVoVtaFdMfGqSg8gbQuS8IxDsIICDxQMIcmygcFDeCHFEl3EfSS1eq6vmH10iOfwkzgnMs2445uxYD0qrYwrZD5ZdXmX4ZrQs9zDCZnpPE81Ut4Ccdahg1_rTm7hhpixnKWxTz1v87tYK8R2r7El0OKbndTRAK7oiHGmSBzdpHtgn5LiP1VR7JT-_aVDphpzoFlFnl6xpdwkElThnialhfYMII0qK3bjL80D6MwkWIHkeWQxWAUpqSci23MXWjqhT_Il5w4w7ooZS_XNI8Crl8O9w76Mh-taAOE0TtBI3BkAqcE=')

# Create the sqlalchemy engine
DATABASE_URL = f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
engine = create_engine(DATABASE_URL)