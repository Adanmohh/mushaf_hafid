import sqlite3
import json
import os

def create_qul_database():
    """Create QUL-compatible database following newinfo.md structure"""
    
    db_path = 'app/database/qul_quran.db'
    
    # Create the database directory if it doesn't exist
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    # Remove existing database if it exists
    if os.path.exists(db_path):
        os.remove(db_path)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create pages table following QUL structure
    cursor.execute('''
        CREATE TABLE pages (
            page_number INTEGER,
            line_number INTEGER,
            line_type TEXT,  -- 'surah_name', 'ayah', 'basmallah'
            is_centered INTEGER,  -- 0 or 1 (boolean)
            first_word_id INTEGER,
            last_word_id INTEGER,
            surah_number INTEGER,
            PRIMARY KEY (page_number, line_number)
        )
    ''')
    
    # Create words table following QUL structure
    cursor.execute('''
        CREATE TABLE words (
            word_index INTEGER PRIMARY KEY,
            word_key TEXT,  -- "surah:ayah" format
            surah INTEGER,
            ayah INTEGER,
            text TEXT
        )
    ''')
    
    # Create surah_names table
    cursor.execute('''
        CREATE TABLE surah_names (
            surah_number INTEGER PRIMARY KEY,
            name_arabic TEXT,
            name_english TEXT,
            total_ayahs INTEGER
        )
    ''')
    
    # Insert Surah names (first 10 surahs for demo)
    surah_data = [
        (1, "الفاتحة", "Al-Fatiha", 7),
        (2, "البقرة", "Al-Baqarah", 286),
        (3, "آل عمران", "Ali 'Imran", 200),
        (4, "النساء", "An-Nisa", 176),
        (5, "المائدة", "Al-Ma'idah", 120),
        (6, "الأنعام", "Al-An'am", 165),
        (7, "الأعراف", "Al-A'raf", 206),
        (8, "الأنفال", "Al-Anfal", 75),
        (9, "التوبة", "At-Tawbah", 129),
        (10, "يونس", "Yunus", 109)
    ]
    
    cursor.executemany('''
        INSERT INTO surah_names (surah_number, name_arabic, name_english, total_ayahs)
        VALUES (?, ?, ?, ?)
    ''', surah_data)
    
    # Insert Al-Fatiha words with proper QUL structure
    fatiha_words = [
        (1, "1:1", 1, 1, "بِسۡمِ"),
        (2, "1:1", 1, 1, "ٱللَّهِ"),
        (3, "1:1", 1, 1, "ٱلرَّحۡمَٰنِ"),
        (4, "1:1", 1, 1, "ٱلرَّحِيمِ"),
        (5, "1:1", 1, 1, "١"),  # Ayah number
        (6, "1:2", 1, 2, "ٱلۡحَمۡدُ"),
        (7, "1:2", 1, 2, "لِلَّهِ"),
        (8, "1:2", 1, 2, "رَبِّ"),
        (9, "1:2", 1, 2, "ٱلۡعَٰلَمِينَ"),
        (10, "1:2", 1, 2, "٢"),
        (11, "1:3", 1, 3, "ٱلرَّحۡمَٰنِ"),
        (12, "1:3", 1, 3, "ٱلرَّحِيمِ"),
        (13, "1:3", 1, 3, "٣"),
        (14, "1:4", 1, 4, "مَٰلِكِ"),
        (15, "1:4", 1, 4, "يَوۡمِ"),
        (16, "1:4", 1, 4, "ٱلدِّينِ"),
        (17, "1:4", 1, 4, "٤"),
        (18, "1:5", 1, 5, "إِيَّاكَ"),
        (19, "1:5", 1, 5, "نَعۡبُدُ"),
        (20, "1:5", 1, 5, "وَإِيَّاكَ"),
        (21, "1:5", 1, 5, "نَسۡتَعِينُ"),
        (22, "1:5", 1, 5, "٥"),
        (23, "1:6", 1, 6, "ٱهۡدِنَا"),
        (24, "1:6", 1, 6, "ٱلصِّرَٰطَ"),
        (25, "1:6", 1, 6, "ٱلۡمُسۡتَقِيمَ"),
        (26, "1:6", 1, 6, "٦"),
        (27, "1:7", 1, 7, "صِرَٰطَ"),
        (28, "1:7", 1, 7, "ٱلَّذِينَ"),
        (29, "1:7", 1, 7, "أَنۡعَمۡتَ"),
        (30, "1:7", 1, 7, "عَلَيۡهِمۡ"),
        (31, "1:7", 1, 7, "غَيۡرِ"),
        (32, "1:7", 1, 7, "ٱلۡمَغۡضُوبِ"),
        (33, "1:7", 1, 7, "عَلَيۡهِمۡ"),
        (34, "1:7", 1, 7, "وَلَا"),
        (35, "1:7", 1, 7, "ٱلضَّآلِّينَ"),
        (36, "1:7", 1, 7, "٧")
    ]
    
    cursor.executemany('''
        INSERT INTO words (word_index, word_key, surah, ayah, text)
        VALUES (?, ?, ?, ?, ?)
    ''', fatiha_words)
    
    # Insert Al-Baqarah first few words for demonstration
    baqarah_start_words = [
        (37, "2:1", 2, 1, "الۤمۤ"),
        (38, "2:1", 2, 1, "١"),
        (39, "2:2", 2, 2, "ذَٰلِكَ"),
        (40, "2:2", 2, 2, "ٱلۡكِتَٰبُ"),
        (41, "2:2", 2, 2, "لَا"),
        (42, "2:2", 2, 2, "رَيۡبَ"),
        (43, "2:2", 2, 2, "فِيهِ"),
        (44, "2:2", 2, 2, "هُدًى"),
        (45, "2:2", 2, 2, "لِّلۡمُتَّقِينَ"),
        (46, "2:2", 2, 2, "٢")
    ]
    
    cursor.executemany('''
        INSERT INTO words (word_index, word_key, surah, ayah, text)
        VALUES (?, ?, ?, ?, ?)
    ''', baqarah_start_words)
    
    # Create page layout following QUL rendering logic from newinfo.md
    # Page 1: Al-Fatiha
    page1_layout = [
        (1, 1, 'surah_name', 1, None, None, 1),
        (1, 2, 'basmallah', 1, 1, 4, None),
        (1, 3, 'ayah', 1, 6, 10, None),
        (1, 4, 'ayah', 1, 11, 13, None),
        (1, 5, 'ayah', 1, 14, 17, None),
        (1, 6, 'ayah', 1, 18, 22, None),
        (1, 7, 'ayah', 1, 23, 26, None),
        (1, 8, 'ayah', 1, 27, 36, None)
    ]
    
    # Page 2: Start of Al-Baqarah  
    page2_layout = [
        (2, 1, 'surah_name', 1, None, None, 2),
        (2, 2, 'ayah', 1, 37, 38, None),
        (2, 3, 'ayah', 1, 39, 46, None)
    ]
    
    all_layouts = page1_layout + page2_layout
    
    cursor.executemany('''
        INSERT INTO pages (page_number, line_number, line_type, is_centered, first_word_id, last_word_id, surah_number)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', all_layouts)
    
    # Create indexes for performance
    cursor.execute('CREATE INDEX idx_words_surah_ayah ON words(surah, ayah)')
    cursor.execute('CREATE INDEX idx_words_index ON words(word_index)')
    cursor.execute('CREATE INDEX idx_pages_page ON pages(page_number)')
    
    conn.commit()
    conn.close()
    
    print(f"QUL database created successfully at {db_path}")
    print(f"Added {len(fatiha_words + baqarah_start_words)} words")
    print(f"Added {len(all_layouts)} page lines")
    print(f"Added {len(surah_data)} surahs")

if __name__ == "__main__":
    create_qul_database() 