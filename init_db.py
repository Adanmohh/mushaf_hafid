"""
Database initialization script
Creates all necessary tables for the Quranic Mushaf API
"""

import sqlite3
import os

def create_database():
    """Create database and all tables"""
    
    # Ensure database directory exists
    db_dir = os.path.dirname("app/database/quran.db")
    os.makedirs(db_dir, exist_ok=True)
    
    # Connect to database
    conn = sqlite3.connect("app/database/quran.db")
    cursor = conn.cursor()
    
    # Create mushaf_layouts table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mushaf_layouts (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            total_pages INTEGER NOT NULL,
            lines_per_page INTEGER NOT NULL,
            font_name TEXT NOT NULL
        )
    """)
    
    # Create pages table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pages (
            id INTEGER PRIMARY KEY,
            mushaf_layout_id INTEGER NOT NULL,
            page_number INTEGER NOT NULL,
            image_url TEXT,
            FOREIGN KEY (mushaf_layout_id) REFERENCES mushaf_layouts(id)
        )
    """)
    
    # Create lines table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lines (
            id INTEGER PRIMARY KEY,
            page_id INTEGER NOT NULL,
            line_number INTEGER NOT NULL,
            FOREIGN KEY (page_id) REFERENCES pages(id)
        )
    """)
    
    # Create words table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS words (
            id INTEGER PRIMARY KEY,
            line_id INTEGER NOT NULL,
            word_position INTEGER NOT NULL,
            surah_number INTEGER NOT NULL,
            ayah_number INTEGER NOT NULL,
            word_text_uthmani TEXT NOT NULL,
            translation_en TEXT,
            transliteration_en TEXT,
            FOREIGN KEY (line_id) REFERENCES lines(id)
        )
    """)
    
    # Create word_positions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS word_positions (
            id INTEGER PRIMARY KEY,
            word_id INTEGER NOT NULL,
            mushaf_layout_id INTEGER NOT NULL,
            page_number INTEGER NOT NULL,
            line_number INTEGER NOT NULL,
            x_coordinate INTEGER NOT NULL,
            y_coordinate INTEGER NOT NULL,
            width INTEGER NOT NULL,
            height INTEGER NOT NULL,
            FOREIGN KEY (word_id) REFERENCES words(id),
            FOREIGN KEY (mushaf_layout_id) REFERENCES mushaf_layouts(id)
        )
    """)
    
    # Create recitations table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS recitations (
            id INTEGER PRIMARY KEY,
            reciter_name TEXT NOT NULL,
            style TEXT NOT NULL
        )
    """)
    
    # Create audio_timings table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS audio_timings (
            id INTEGER PRIMARY KEY,
            word_id INTEGER NOT NULL,
            recitation_id INTEGER NOT NULL,
            start_time INTEGER NOT NULL,
            end_time INTEGER NOT NULL,
            audio_file_url TEXT NOT NULL,
            FOREIGN KEY (word_id) REFERENCES words(id),
            FOREIGN KEY (recitation_id) REFERENCES recitations(id)
        )
    """)
    
    # Create indexes for better performance
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_words_surah_ayah ON words(surah_number, ayah_number)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_words_text ON words(word_text_uthmani)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_words_translation ON words(translation_en)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_word_positions_layout_page ON word_positions(mushaf_layout_id, page_number)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_audio_timings_word_recitation ON audio_timings(word_id, recitation_id)")
    
    # Commit changes
    conn.commit()
    conn.close()
    
    print("Database created successfully!")

if __name__ == "__main__":
    create_database()

