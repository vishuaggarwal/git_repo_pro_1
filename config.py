# config.py
from dotenv import load_dotenv
from sqlalchemy import create_engine
import os
load_dotenv()

db_uri = 'sqlite:///data.db'
engine = create_engine(db_uri)


DB_URI = os.getenv('DB_URI')


api_id = 20254122
api_hash = 'b966c845c8ba8fb3b7f5d812c51ec832'


db_uri = 'sqlite:///app.db'





