"""
Database connection and configuration
"""

import sqlite3
import aiosqlite
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Database configuration
DATABASE_URL = "sqlite:///./app/database/quran.db"
DATABASE_PATH = "./app/database/quran.db"

# SQLAlchemy setup
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

async def init_database():
    """Initialize database with tables and sample data"""
    # Create database directory if it doesn't exist
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Check if database is empty and populate with sample data
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute("SELECT COUNT(*) FROM mushaf_layouts")
        count = await cursor.fetchone()
        
        if count[0] == 0:
            await populate_sample_data(db)

async def populate_sample_data(db):
    """Populate database with sample data"""
    
    # Insert sample Mushaf layout
    await db.execute("""
        INSERT INTO mushaf_layouts (id, name, total_pages, lines_per_page, font_name)
        VALUES (1, 'Uthmani Hafs', 604, 15, 'me_quran')
    """)
    
    # Insert sample pages (first few pages)
    for page_num in range(1, 6):
        await db.execute("""
            INSERT INTO pages (mushaf_layout_id, page_number, image_url)
            VALUES (1, ?, ?)
        """, (page_num, f"/static/images/page_{page_num:03d}.png"))
    
    # Insert sample lines for page 1
    for line_num in range(1, 16):
        await db.execute("""
            INSERT INTO lines (page_id, line_number)
            VALUES (1, ?)
        """, (line_num,))
    
    # Insert sample words for Al-Fatiha (first few words)
    sample_words = [
        (1, 1, 1, 1, "بِسْمِ", "In the name", "Bismi"),
        (1, 2, 1, 1, "ٱللَّهِ", "of Allah", "Allahi"),
        (1, 3, 1, 1, "ٱلرَّحْمَـٰنِ", "the Most Gracious", "Ar-Rahmani"),
        (1, 4, 1, 1, "ٱلرَّحِيمِ", "the Most Merciful", "Ar-Raheem"),
        (2, 1, 1, 2, "ٱلْحَمْدُ", "All praise", "Al-hamdu"),
        (2, 2, 1, 2, "لِلَّهِ", "is for Allah", "lillahi"),
        (2, 3, 1, 2, "رَبِّ", "Lord", "rabbi"),
        (2, 4, 1, 2, "ٱلْعَـٰلَمِينَ", "of the worlds", "al-alameen"),
    ]
    
    for line_id, word_pos, surah, ayah, text, translation, transliteration in sample_words:
        await db.execute("""
            INSERT INTO words (line_id, word_position, surah_number, ayah_number, 
                             word_text_uthmani, translation_en, transliteration_en)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (line_id, word_pos, surah, ayah, text, translation, transliteration))
    
    # Insert sample word positions
    sample_positions = [
        (1, 1, 1, 1, 100, 50, 40, 20),
        (2, 1, 1, 1, 150, 50, 45, 20),
        (3, 1, 1, 1, 200, 50, 60, 20),
        (4, 1, 1, 1, 270, 50, 50, 20),
        (5, 1, 1, 2, 100, 80, 50, 20),
        (6, 1, 1, 2, 160, 80, 35, 20),
        (7, 1, 1, 2, 200, 80, 30, 20),
        (8, 1, 1, 2, 240, 80, 70, 20),
    ]
    
    for word_id, layout_id, page, line, x, y, w, h in sample_positions:
        await db.execute("""
            INSERT INTO word_positions (word_id, mushaf_layout_id, page_number, 
                                      line_number, x_coordinate, y_coordinate, width, height)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (word_id, layout_id, page, line, x, y, w, h))
    
    # Insert sample recitation
    await db.execute("""
        INSERT INTO recitations (id, reciter_name, style)
        VALUES (1, 'Abdul Basit Abdul Samad', 'Murattal')
    """)
    
    # Insert sample audio timings
    sample_timings = [
        (1, 1, 1000, 1500, "/static/audio/001001_abdul_basit.mp3"),
        (2, 1, 1500, 2200, "/static/audio/001001_abdul_basit.mp3"),
        (3, 1, 2200, 3000, "/static/audio/001001_abdul_basit.mp3"),
        (4, 1, 3000, 3600, "/static/audio/001001_abdul_basit.mp3"),
        (5, 1, 4000, 4500, "/static/audio/001002_abdul_basit.mp3"),
        (6, 1, 4500, 5000, "/static/audio/001002_abdul_basit.mp3"),
        (7, 1, 5000, 5300, "/static/audio/001002_abdul_basit.mp3"),
        (8, 1, 5300, 6200, "/static/audio/001002_abdul_basit.mp3"),
    ]
    
    for word_id, rec_id, start, end, audio_url in sample_timings:
        await db.execute("""
            INSERT INTO audio_timings (word_id, recitation_id, start_time, end_time, audio_file_url)
            VALUES (?, ?, ?, ?, ?)
        """, (word_id, rec_id, start, end, audio_url))
    
    await db.commit()

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_async_db():
    """Get async database connection"""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        yield db

