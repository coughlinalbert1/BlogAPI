from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os




# SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'
#SQLALCHEMY_DATABASE_URL="postgresql://postgres:password123@db:5432/dockert"
#                         postgresql://None:password123@db:5432/dockert
SQLALCHEMY_DATABASE_URL = f'postgresql://{os.getenv("DATABASE_USERNAME")}:{os.getenv("DATABASE_PASSWORD")}@{os.getenv("DATABASE_HOSTNAME")}:{os.getenv("DATABASE_PORT")}/{os.getenv("DATABASE_NAME")}'
print(SQLALCHEMY_DATABASE_URL)  # For debugging purposes, remove later



engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

Base = declarative_base()

def get_db():
    """
    Returns a database session.

    Yields:
        Session: The database session.

    Raises:
        None

    Returns:
        Session: The database session.

    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()