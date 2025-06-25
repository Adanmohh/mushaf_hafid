"""
QUL-compatible database schema and initialization
Based on QUL Mushaf Layout structure
"""

import sqlite3
import os

def create_qul_database():
    """Create QUL-compatible database with proper schema"""
    
    # Ensure database directory exists
    db_dir = os.path.dirname("app/database/qul_quran.db")
    os.makedirs(db_dir, exist_ok=True)
    
    # Connect to database
    conn = sqlite3.connect("app/database/qul_quran.db")
    cursor = conn.cursor()
    
    # Create pages table (QUL Mushaf Layout structure)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            page_number INTEGER NOT NULL,
            line_number INTEGER NOT NULL,
            line_type TEXT NOT NULL CHECK (line_type IN ('ayah', 'surah_name', 'basmallah')),
            is_centered BOOLEAN NOT NULL DEFAULT 1,
            first_word_id INTEGER,
            last_word_id INTEGER,
            surah_number INTEGER,
            UNIQUE(page_number, line_number)
        )
    """)
    
    # Create words table (QUL Quran Script structure)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS words (
            word_index INTEGER PRIMARY KEY,
            word_key TEXT NOT NULL,
            surah INTEGER NOT NULL,
            ayah INTEGER NOT NULL,
            text TEXT NOT NULL
        )
    """)
    
    # Create surah_names table (QUL Metadata structure)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS surah_names (
            surah_number INTEGER PRIMARY KEY,
            name_arabic TEXT NOT NULL,
            name_english TEXT NOT NULL,
            total_ayahs INTEGER NOT NULL
        )
    """)
    
    # Create indexes for better performance
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_pages_page_number ON pages(page_number)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_pages_line_number ON pages(page_number, line_number)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_words_surah_ayah ON words(surah, ayah)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_words_index ON words(word_index)")
    
    # Commit changes
    conn.commit()
    conn.close()
    
    print("QUL-compatible database created successfully!")

def add_sample_qul_data():
    """Add sample data in QUL format for Al-Fatiha"""
    
    conn = sqlite3.connect("app/database/qul_quran.db")
    cursor = conn.cursor()
    
    # Add surah names
    surah_names_data = [
        (1, "الفاتحة", "Al-Fatiha", 7),
        (2, "البقرة", "Al-Baqarah", 286),
        (3, "آل عمران", "Ali 'Imran", 200)
    ]
    
    cursor.executemany("""
        INSERT OR REPLACE INTO surah_names 
        (surah_number, name_arabic, name_english, total_ayahs)
        VALUES (?, ?, ?, ?)
    """, surah_names_data)
    
    # Add words for Al-Fatiha (word_index matches QUL format)
    words_data = [
        # Bismillah
        (1, "1:1:1", 1, 1, "بِسۡمِ"),
        (2, "1:1:2", 1, 1, "ٱللَّهِ"),
        (3, "1:1:3", 1, 1, "ٱلرَّحۡمَٰنِ"),
        (4, "1:1:4", 1, 1, "ٱلرَّحِيمِ"),
        
        # Verse 2
        (5, "1:2:1", 1, 2, "ٱلۡحَمۡدُ"),
        (6, "1:2:2", 1, 2, "لِلَّهِ"),
        (7, "1:2:3", 1, 2, "رَبِّ"),
        (8, "1:2:4", 1, 2, "ٱلۡعَٰلَمِينَ"),
        
        # Verse 3
        (9, "1:3:1", 1, 3, "ٱلرَّحۡمَٰنِ"),
        (10, "1:3:2", 1, 3, "ٱلرَّحِيمِ"),
        
        # Verse 4
        (11, "1:4:1", 1, 4, "مَٰلِكِ"),
        (12, "1:4:2", 1, 4, "يَوۡمِ"),
        (13, "1:4:3", 1, 4, "ٱلدِّينِ"),
        
        # Verse 5
        (14, "1:5:1", 1, 5, "إِيَّاكَ"),
        (15, "1:5:2", 1, 5, "نَعۡبُدُ"),
        (16, "1:5:3", 1, 5, "وَإِيَّاكَ"),
        (17, "1:5:4", 1, 5, "نَسۡتَعِينُ"),
        
        # Verse 6
        (18, "1:6:1", 1, 6, "ٱهۡدِنَا"),
        (19, "1:6:2", 1, 6, "ٱلصِّرَٰطَ"),
        (20, "1:6:3", 1, 6, "ٱلۡمُسۡتَقِيمَ"),
        
        # Verse 7
        (21, "1:7:1", 1, 7, "صِرَٰطَ"),
        (22, "1:7:2", 1, 7, "ٱلَّذِينَ"),
        (23, "1:7:3", 1, 7, "أَنۡعَمۡتَ"),
        (24, "1:7:4", 1, 7, "عَلَيۡهِمۡ"),
        (25, "1:7:5", 1, 7, "غَيۡرِ"),
        (26, "1:7:6", 1, 7, "ٱلۡمَغۡضُوبِ"),
        (27, "1:7:7", 1, 7, "عَلَيۡهِمۡ"),
        (28, "1:7:8", 1, 7, "وَلَا"),
        (29, "1:7:9", 1, 7, "ٱلضَّآلِّينَ")
    ]
    
    cursor.executemany("""
        INSERT OR REPLACE INTO words 
        (word_index, word_key, surah, ayah, text)
        VALUES (?, ?, ?, ?, ?)
    """, words_data)
    
    # Add page layout for Al-Fatiha (Page 1 in most Mushafs)
    pages_data = [
        # Page 1 - Al-Fatiha
        (1, 1, 'surah_name', True, None, None, 1),      # Surah name
        (1, 2, 'ayah', True, 1, 4, 1),                  # Bismillah (1:1)
        (1, 3, 'ayah', True, 5, 8, 1),                  # Verse 2
        (1, 4, 'ayah', True, 9, 10, 1),                 # Verse 3
        (1, 5, 'ayah', True, 11, 13, 1),                # Verse 4
        (1, 6, 'ayah', True, 14, 17, 1),                # Verse 5
        (1, 7, 'ayah', True, 18, 20, 1),                # Verse 6
        (1, 8, 'ayah', True, 21, 24, 1),                # Verse 7a
        (1, 9, 'ayah', True, 25, 29, 1),                # Verse 7b
    ]
    
    for page_data in pages_data:
        cursor.execute("""
            INSERT OR REPLACE INTO pages 
            (page_number, line_number, line_type, is_centered, first_word_id, last_word_id, surah_number)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, page_data)
    
    conn.commit()
    conn.close()
    
    print("Sample QUL data for Al-Fatiha added successfully!")

if __name__ == "__main__":
    create_qul_database()
    add_sample_qul_data()