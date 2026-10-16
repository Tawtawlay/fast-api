# Imports the function used to create a database engine
from sqlalchemy import create_engine
# Imports tools for creating database sessions and defining models
from sqlalchemy.orm import sessionmaker, declarative_base


# Creates a variable that stores the address of our database (SQLite)
SQLALCHEMY_DATABASE_URL = 'sqlite:///./todos.db'


# Creates an engine that manages connections to our database
# check_same_thread=False allows SQLite connections to be used across threads
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})

# Creates a factory that will produce new database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Creates a base class for our SQLAlchemy models.
# SQLAlchemy uses this base to track model definitions and their tables.
Base = declarative_base()

