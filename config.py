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
