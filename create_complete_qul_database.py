import sqlite3
import os
import shutil

def create_complete_qul_database():
    """Create complete QUL database using real QUL resources"""
    
    # Database paths
    source_paths = {
        'words': 'qul_guide/Quran_script_in_word_by_word_format.db',
        'layout': 'qul_guide/qpc-hafs-15-lines.db',
        'surah_names': 'qul_guide/quran-metadata-surah-name.sqlite'
    }
    
    target_db = 'app/database/qul_complete.db'
    
    print("🏗️ CREATING COMPLETE QUL DATABASE")
    print("=" * 60)
    
    # Create target directory
    os.makedirs(os.path.dirname(target_db), exist_ok=True)
    
    # Remove existing database
    if os.path.exists(target_db):
        os.remove(target_db)
        print("🗑️ Removed existing database")
    
    # Create new database
    conn = sqlite3.connect(target_db)
    cursor = conn.cursor()
    
    try:
        # 1. Create and populate words table
        print("\n📝 Creating words table...")
        cursor.execute('''
            CREATE TABLE words (
                id INTEGER PRIMARY KEY,
                location TEXT,
                surah INTEGER,
                ayah INTEGER,
                word INTEGER,
                text TEXT
            )
        ''')
        
        # Copy words from source
        words_conn = sqlite3.connect(source_paths['words'])
        words_cursor = words_conn.cursor()
        words_cursor.execute("SELECT * FROM words")
        words_data = words_cursor.fetchall()
        
        cursor.executemany('''
            INSERT INTO words (id, location, surah, ayah, word, text)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', words_data)
        
        words_conn.close()
        print(f"   ✅ Inserted {len(words_data)} words")
        
        # 2. Create and populate pages table
        print("\n📄 Creating pages table...")
        cursor.execute('''
            CREATE TABLE pages (
                page_number INTEGER,
                line_number INTEGER,
                line_type TEXT,
                is_centered INTEGER,
                first_word_id INTEGER,
                last_word_id INTEGER,
                surah_number INTEGER
            )
        ''')
        
        # Copy pages from layout source
        layout_conn = sqlite3.connect(source_paths['layout'])
        layout_cursor = layout_conn.cursor()
        layout_cursor.execute("SELECT * FROM pages")
        pages_data = layout_cursor.fetchall()
        
        cursor.executemany('''
            INSERT INTO pages (page_number, line_number, line_type, is_centered, 
                             first_word_id, last_word_id, surah_number)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', pages_data)
        
        layout_conn.close()
        print(f"   ✅ Inserted {len(pages_data)} page lines")
        
        # 3. Create and populate chapters (surah names) table
        print("\n📚 Creating chapters table...")
        cursor.execute('''
            CREATE TABLE chapters (
                id INTEGER PRIMARY KEY,
                name TEXT,
                name_simple TEXT,
                name_arabic TEXT,
                revelation_order INTEGER,
                revelation_place TEXT,
                verses_count INTEGER,
                bismillah_pre INTEGER
            )
        ''')
        
        # Copy chapters from source
        chapters_conn = sqlite3.connect(source_paths['surah_names'])
        chapters_cursor = chapters_conn.cursor()
        chapters_cursor.execute("SELECT * FROM chapters")
        chapters_data = chapters_cursor.fetchall()
        
        cursor.executemany('''
            INSERT INTO chapters (id, name, name_simple, name_arabic, 
                                revelation_order, revelation_place, verses_count, bismillah_pre)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', chapters_data)
        
        chapters_conn.close()
        print(f"   ✅ Inserted {len(chapters_data)} chapters")
        
        # 4. Create layout info table
        print("\n📋 Creating layout info...")
        cursor.execute('''
            CREATE TABLE layout_info (
                name TEXT,
                number_of_pages INTEGER,
                lines_per_page INTEGER,
                font_name TEXT
            )
        ''')
        
        cursor.execute('''
            INSERT INTO layout_info (name, number_of_pages, lines_per_page, font_name)
            VALUES ('QPC HAFS Complete', 604, 15, 'qpc-hafs-page-specific')
        ''')
        
        print("   ✅ Created layout info")
        
        # 5. Create indexes for performance
        print("\n🔗 Creating database indexes...")
        indexes = [
            "CREATE INDEX idx_words_surah_ayah ON words(surah, ayah)",
            "CREATE INDEX idx_words_id ON words(id)",
            "CREATE INDEX idx_pages_page_number ON pages(page_number)",
            "CREATE INDEX idx_pages_word_range ON pages(first_word_id, last_word_id)",
            "CREATE INDEX idx_chapters_id ON chapters(id)"
        ]
        
        for index_sql in indexes:
            cursor.execute(index_sql)
        
        print("   ✅ Created performance indexes")
        
        # Commit all changes
        conn.commit()
        
        # 6. Verify the database
        print("\n🔍 Verifying database...")
        
        # Check word count
        cursor.execute("SELECT COUNT(*) FROM words")
        word_count = cursor.fetchone()[0]
        
        # Check page count
        cursor.execute("SELECT COUNT(DISTINCT page_number) FROM pages")
        page_count = cursor.fetchone()[0]
        
        # Check chapter count
        cursor.execute("SELECT COUNT(*) FROM chapters")
        chapter_count = cursor.fetchone()[0]
        
        # Check page range
        cursor.execute("SELECT MIN(page_number), MAX(page_number) FROM pages")
        min_page, max_page = cursor.fetchone()
        
        # Check surah range
        cursor.execute("SELECT MIN(surah), MAX(surah) FROM words")
        min_surah, max_surah = cursor.fetchone()
        
        print(f"   📊 Words: {word_count:,}")
        print(f"   📄 Pages: {page_count} (range: {min_page}-{max_page})")
        print(f"   📚 Chapters: {chapter_count}")
        print(f"   🕌 Surahs: {min_surah}-{max_surah}")
        
        print(f"\n✅ Database created successfully: {target_db}")
        print(f"📏 Database size: {os.path.getsize(target_db) / (1024*1024):.1f} MB")
        
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        conn.close()

def test_database():
    """Test the created database with sample queries"""
    db_path = 'app/database/qul_complete.db'
    
    if not os.path.exists(db_path):
        print("❌ Database not found for testing")
        return
    
    print(f"\n🧪 TESTING DATABASE")
    print("=" * 40)
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Test 1: Get first page
        print("📄 Testing page 1 retrieval...")
        cursor.execute('''
            SELECT line_number, line_type, is_centered, first_word_id, last_word_id, surah_number
            FROM pages 
            WHERE page_number = 1 
            ORDER BY line_number
        ''')
        page_1_lines = cursor.fetchall()
        print(f"   Page 1 has {len(page_1_lines)} lines")
        
        # Test 2: Get words for first line of page 1
        if page_1_lines:
            line = page_1_lines[1]  # Second line (first ayah line)
            if line[3] and line[4]:  # first_word_id and last_word_id
                cursor.execute('''
                    SELECT text FROM words 
                    WHERE id BETWEEN ? AND ?
                    ORDER BY id
                ''', (line[3], line[4]))
                words = cursor.fetchall()
                word_text = ' '.join([w[0] for w in words])
                print(f"   First ayah line: {word_text}")
        
        # Test 3: Get Al-Fatiha info
        cursor.execute("SELECT name_simple, name_arabic, verses_count FROM chapters WHERE id = 1")
        fatiha_info = cursor.fetchone()
        print(f"   Al-Fatiha: {fatiha_info[0]} ({fatiha_info[1]}) - {fatiha_info[2]} verses")
        
        # Test 4: Check total Quran stats
        cursor.execute("SELECT COUNT(*) FROM words")
        total_words = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(DISTINCT page_number) FROM pages")
        total_pages = cursor.fetchone()[0]
        
        print(f"   📊 Total: {total_words:,} words across {total_pages} pages")
        
        conn.close()
        print("✅ Database tests passed!")
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    create_complete_qul_database()
    test_database() 