# utils/db.py

# Declares a base class for declarative SQLAlchemy models using 
# sqlalchemy.ext.declarative. Allows subclasses to be mapped 
# to relational database tables.
# utils/db.py

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


engine = create_engine(db_uri)