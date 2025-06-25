"""
Test script to verify database and data
"""

import sqlite3
import os

def test_database():
    """Test database connectivity and data"""
    
    db_path = "app/database/quran.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Database not found at {db_path}")
        return False
    
    print(f"✅ Database found at {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Test layouts
        cursor.execute("SELECT COUNT(*) FROM mushaf_layouts")
        layout_count = cursor.fetchone()[0]
        print(f"✅ Layouts: {layout_count}")
        
        # Test words
        cursor.execute("SELECT COUNT(*) FROM words")
        word_count = cursor.fetchone()[0]
        print(f"✅ Words: {word_count}")
        
        # Test word positions
        cursor.execute("SELECT COUNT(*) FROM word_positions")
        position_count = cursor.fetchone()[0]
        print(f"✅ Word positions: {position_count}")
        
        # Test sample Al-Fatiha data
        cursor.execute("""
            SELECT w.word_text_uthmani, w.translation_en, wp.x_coordinate, wp.y_coordinate
            FROM words w
            JOIN word_positions wp ON w.id = wp.word_id
            WHERE w.surah_number = 1 AND w.ayah_number = 1
            ORDER BY w.word_position
        """)
        
        fatiha_words = cursor.fetchall()
        print(f"✅ Al-Fatiha Bismillah words: {len(fatiha_words)}")
        
        if fatiha_words:
            print("\nSample Al-Fatiha data:")
            for word in fatiha_words[:4]:  # First 4 words of Bismillah
                print(f"  {word[0]} ({word[1]}) at position ({word[2]}, {word[3]})")
        
        # Test audio timings
        cursor.execute("SELECT COUNT(*) FROM audio_timings")
        audio_count = cursor.fetchone()[0]
        print(f"✅ Audio timings: {audio_count}")
        
        conn.close()
        print("\n🎉 Database test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

if __name__ == "__main__":
    print("🕌 Testing Mushaf Hafid Database")
    print("=" * 40)
    test_database()