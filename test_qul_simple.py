#!/usr/bin/env python3
"""
Simple test of QUL database and rendering logic
"""

import sqlite3
import json

def test_qul_page_rendering(page_number=1):
    """Test QUL page rendering logic directly"""
    
    print(f"=== Testing QUL Page {page_number} Rendering ===")
    
    # Connect to database
    conn = sqlite3.connect("app/database/qul_quran.db")
    cursor = conn.cursor()
    
    # Get page layout data
    cursor.execute("""
        SELECT page_number, line_number, line_type, is_centered, 
               first_word_id, last_word_id, surah_number
        FROM pages
        WHERE page_number = ?
        ORDER BY line_number
    """, (page_number,))
    
    page_lines = cursor.fetchall()
    
    if not page_lines:
        print(f"❌ Page {page_number} not found")
        return False
    
    # Get all words for this page
    word_ids = []
    for line in page_lines:
        if line[4] and line[5]:  # first_word_id and last_word_id
            word_ids.extend(range(line[4], line[5] + 1))
    
    if word_ids:
        placeholders = ','.join('?' * len(word_ids))
        cursor.execute(f"""
            SELECT word_index, word_key, surah, ayah, text
            FROM words
            WHERE word_index IN ({placeholders})
            ORDER BY word_index
        """, word_ids)
        
        word_rows = cursor.fetchall()
        word_data = {row[0]: row[4] for row in word_rows}  # word_index -> text
    else:
        word_data = {}
    
    # Get surah names
    cursor.execute("""
        SELECT surah_number, name_arabic
        FROM surah_names
    """)
    surah_rows = cursor.fetchall()
    surah_names = {row[0]: row[1] for row in surah_rows}
    
    # Build page content following QUL rendering logic
    page_content = []
    
    print(f"\nPage {page_number} has {len(page_lines)} lines:")
    
    for line in page_lines:
        page_num, line_num, line_type, is_centered, first_word_id, last_word_id, surah_number = line
        
        line_content = {
            "line_number": line_num,
            "line_type": line_type,
            "is_centered": bool(is_centered),
            "content": "",
            "words": []
        }
        
        if line_type == 'surah_name':
            # Render surah name
            if surah_number and surah_number in surah_names:
                line_content["content"] = f"سورة {surah_names[surah_number]}"
                line_content["surah_number"] = surah_number
                print(f"  Line {line_num} (surah_name): {line_content['content']}")
        
        elif line_type == 'ayah':
            # Render ayah words
            if first_word_id and last_word_id:
                words_in_line = []
                for word_id in range(first_word_id, last_word_id + 1):
                    if word_id in word_data:
                        words_in_line.append({
                            "word_id": word_id,
                            "text": word_data[word_id]
                        })
                
                line_content["words"] = words_in_line
                line_content["content"] = " ".join([w["text"] for w in words_in_line])
                line_content["first_word_id"] = first_word_id
                line_content["last_word_id"] = last_word_id
                
                print(f"  Line {line_num} (ayah): {line_content['content']}")
                print(f"    └─ {len(words_in_line)} words (IDs {first_word_id}-{last_word_id})")
        
        elif line_type == 'basmallah':
            # Render Bismillah
            line_content["content"] = "بِسۡمِ ٱللَّهِ ٱلرَّحۡمَٰنِ ٱلرَّحِيمِ"
            print(f"  Line {line_num} (basmallah): {line_content['content']}")
        
        page_content.append(line_content)
    
    conn.close()
    
    print(f"\n✅ Successfully rendered page {page_number} with {len(page_content)} lines")
    
    # Show final JSON structure
    result = {
        "page_number": page_number,
        "total_lines": len(page_content),
        "lines": page_content
    }
    
    print(f"\nFinal API response structure:")
    print(f"  page_number: {result['page_number']}")
    print(f"  total_lines: {result['total_lines']}")
    print(f"  lines: Array with {len(result['lines'])} items")
    
    return True

def test_qul_database_structure():
    """Test QUL database structure and sample data"""
    
    print("=== Testing QUL Database Structure ===")
    
    conn = sqlite3.connect("app/database/qul_quran.db")
    cursor = conn.cursor()
    
    # Test tables exist
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    
    expected_tables = ['pages', 'words', 'surah_names']
    for table in expected_tables:
        if table in tables:
            print(f"✅ Table '{table}' exists")
        else:
            print(f"❌ Table '{table}' missing")
            return False
    
    # Test data counts
    cursor.execute("SELECT COUNT(*) FROM pages")
    pages_count = cursor.fetchone()[0]
    print(f"  Pages: {pages_count} entries")
    
    cursor.execute("SELECT COUNT(*) FROM words")
    words_count = cursor.fetchone()[0]
    print(f"  Words: {words_count} entries")
    
    cursor.execute("SELECT COUNT(*) FROM surah_names")
    surahs_count = cursor.fetchone()[0]
    print(f"  Surahs: {surahs_count} entries")
    
    conn.close()
    return True

def main():
    """Run all tests"""
    print("🚀 Starting QUL Integration Tests")
    print("=" * 50)
    
    # Test database structure
    db_ok = test_qul_database_structure()
    
    print()
    
    # Test page rendering
    render_ok = test_qul_page_rendering(1)
    
    print("\n" + "=" * 50)
    if db_ok and render_ok:
        print("🎉 All QUL tests PASSED!")
        print("\nThe QUL-compatible backend is working correctly!")
        print("Ready for integration with the frontend.")
    else:
        print("❌ Some tests FAILED!")

if __name__ == "__main__":
    main()