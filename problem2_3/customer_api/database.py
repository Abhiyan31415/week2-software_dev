from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from sqlalchemy.ext.declarative import declarative_base

import os

from logger import logger

load_dotenv()

database_url=os.getenv("DATABASE_URL")
if not database_url:
    logger.error("DATABASE_URL not found in environment variables")
    raise ValueError("DATABASE_URL must be set in .env file")

try:
    engine = create_engine(
        database_url,
        pool_pre_ping=True
    )
    logger.info("Database engine created successfully")
except Exception as e:
    logger.error(f"Failed to create database engine: {e}")
    raise

sessionlocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base = declarative_base()

def get_db():
    """
    Creates a new database session for each request.
    Automatically closes the session after the request completes.
    """
    db = sessionlocal()
    logger.info("Database session created")
    try:
        yield db
    except Exception as e:
        logger.error(f"Database session error: {e}")
        db.rollback()
        raise
    finally:
        db.close()
        logger.info("Database session closed")