"""
Database connection and configuration
"""

import aiosqlite
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

DATABASE_URL = "sqlite:///./app/database/quran.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

async def get_async_db():
    """Get async database connection"""
    db_path = "app/database/quran.db"
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    async with aiosqlite.connect(db_path) as db:
        yield db

async def init_database():
    """Initialize database on startup"""
    db_path = "app/database/quran.db"
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    # Database will be created by init_db.py script
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}. Please run init_db.py first.")
    else:
        print(f"Database found at {db_path}")