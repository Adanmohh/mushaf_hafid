#!/usr/bin/env python3
"""
Test QUL API endpoints directly
"""

import asyncio
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.routers.qul_mushaf import get_qul_page, get_surah_names, get_surah_info
import aiosqlite

async def test_qul_database():
    """Test QUL database connection and basic queries"""
    
    db_path = "app/database/qul_quran.db"
    
    try:
        async with aiosqlite.connect(db_path) as db:
            print("=== Testing QUL Database Connection ===")
            
            # Test surah names
            print("\n1. Testing Surah Names:")
            cursor = await db.execute("SELECT * FROM surah_names")
            rows = await cursor.fetchall()
            for row in rows:
                print(f"  Surah {row[0]}: {row[1]} ({row[2]}) - {row[3]} ayahs")
            
            # Test page 1 layout
            print("\n2. Testing Page 1 Layout:")
            cursor = await db.execute("""
                SELECT page_number, line_number, line_type, is_centered, 
                       first_word_id, last_word_id, surah_number
                FROM pages
                WHERE page_number = 1
                ORDER BY line_number
            """)
            rows = await cursor.fetchall()
            for row in rows:
                print(f"  Line {row[1]}: {row[2]} (centered: {bool(row[3])}) words {row[4]}-{row[5]}")
            
            # Test words for first line
            print("\n3. Testing Words in First Ayah Line:")
            cursor = await db.execute("""
                SELECT word_index, word_key, text
                FROM words
                WHERE word_index BETWEEN 1 AND 4
                ORDER BY word_index
            """)
            rows = await cursor.fetchall()
            combined_text = " ".join([row[2] for row in rows])
            print(f"  Combined text: {combined_text}")
            for row in rows:
                print(f"    Word {row[0]} ({row[1]}): {row[2]}")
                
    except Exception as e:
        print(f"Database test failed: {e}")
        return False
    
    return True

async def test_qul_api_functions():
    """Test QUL API functions directly"""
    
    print("\n=== Testing QUL API Functions ===")
    
    try:
        # Mock database dependency
        async def mock_get_qul_db():
            db_path = "app/database/qul_quran.db"
            async with aiosqlite.connect(db_path) as db:
                yield db
        
        # Test get_surah_names
        print("\n1. Testing get_surah_names:")
        async for db in mock_get_qul_db():
            result = await get_surah_names(db)
            print(f"  Found {len(result['surahs'])} surahs")
            print(f"  First surah: {result['surahs'][0]}")
        
        # Test get_surah_info
        print("\n2. Testing get_surah_info:")
        async for db in mock_get_qul_db():
            result = await get_surah_info(1, db)
            print(f"  Surah info: {result}")
        
        # Test get_qul_page
        print("\n3. Testing get_qul_page for page 1:")
        async for db in mock_get_qul_db():
            result = await get_qul_page(1, db)
            print(f"  Page {result['page_number']} has {result['total_lines']} lines")
            
            for i, line in enumerate(result['lines'][:3]):  # Show first 3 lines
                print(f"    Line {line['line_number']}: {line['line_type']} - '{line['content'][:50]}...'")
                if line['words']:
                    print(f"      Contains {len(line['words'])} words")
                
    except Exception as e:
        print(f"API function test failed: {e}")
        return False
    
    return True

async def main():
    """Run all tests"""
    print("Starting QUL API Tests...")
    
    # Test database
    db_success = await test_qul_database()
    
    # Test API functions
    api_success = await test_qul_api_functions()
    
    if db_success and api_success:
        print("\n✅ All QUL tests passed successfully!")
        print("\nThe QUL-compatible backend is ready and working correctly.")
        print("You can now use the following API endpoints:")
        print("  GET /api/v1/qul/layouts - Get available layouts")
        print("  GET /api/v1/qul/page/1 - Get page 1 (Al-Fatiha)")
        print("  GET /api/v1/qul/surah-names - Get all surah names")
        print("  GET /api/v1/qul/surah/1 - Get surah 1 info")
    else:
        print("\n❌ Some tests failed!")
    
if __name__ == "__main__":
    asyncio.run(main())