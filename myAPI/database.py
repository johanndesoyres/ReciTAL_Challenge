from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Here I choose SQLite because it doesn't require any installation on your side
# if you want to test my API. In a real world I would choose of course a better
# SQL database like PostGreSQL which has many advantages :
#
# - support complex operations
# - easily connectable with others tools and other programming languages
# - support high volumes of data
# - support high concurrency

SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"

# Create a SQL Alchemy engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
# Create a sessionmaker to create later database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Create a base class to create later SQL Alchemy models
Base = declarative_base()
