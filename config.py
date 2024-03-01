# config.py
from dotenv import load_dotenv
from  sqlalchemy import create_engine
import sqlalchemy
import os
load_dotenv()

db_uri = 'mysql+asyncmy://root@localhost:3306/test.db'

def connect_to_db(db_uri):
    try:
        return sqlalchemy.create_engine(db_uri)
    except Exception as e:
        print("Error connecting to database:", e)
        return None


engine = connect_to_db(db_uri)

DB_URI = os.getenv('DB_URI')

api_id = 20254122
api_hash = 'b966c845c8ba8fb3b7f5d812c51ec832'
session_key = '1BVtsOJ0Buwbgwiopb6X3b-mO68dtQboJqg_icCTr21DtRsH5YVoVtaFdMfGqSg8gbQuS8IxDsIICDxQMIcmygcFDeCHFEl3EfSS1eq6vmH10iOfwkzgnMs2445uxYD0qrYwrZD5ZdXmX4ZrQs9zDCZnpPE81Ut4Ccdahg1_rTm7hhpixnKWxTz1v87tYK8R2r7El0OKbndTRAK7oiHGmSBzdpHtgn5LiP1VR7JT-_aVDphpzoFlFnl6xpdwkElThnialhfYMII0qK3bjL80D6MwkWIHkeWQxWAUpqSci23MXWjqhT_Il5w4w7ooZS_XNI8Crl8O9w76Mh-taAOE0TtBI3BkAqcE='

