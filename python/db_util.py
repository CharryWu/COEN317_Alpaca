from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./db/sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

# By default SQLite will only allow one thread to communicate with it,
# assuming that each thread would handle an independent request.
# This is to prevent accidentally sharing the same connection for different things (for different requests).
# But in FastAPI, using normal functions (def) more than one thread could interact
# with the database for the same request,
# so we need to make SQLite know that it should allow that with connect_args={"check_same_thread": False}.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
# once we create an instance of the SessionLocal class,
# this instance will be the actual database session.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # We name it SessionLocal to distinguish it from the Session we are importing from SQLAlchemy.

Base = declarative_base() # Later we will inherit from this class to create each of the database models or classes (the ORM models)

