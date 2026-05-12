from sqlalchemy import create_engine

from dotenv import load_dotenv

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
