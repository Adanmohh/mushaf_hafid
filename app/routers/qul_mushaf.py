"""
QUL-compatible Mushaf router following QUL rendering logic
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any
import aiosqlite
import asyncio

router = APIRouter()

async def get_qul_db():
    """Get QUL database connection"""
    db_path = "app/database/qul_quran.db"
    async with aiosqlite.connect(db_path) as db:
        yield db

@router.get("/layouts")
async def get_qul_layouts():
    """Get available QUL layouts"""
    return {
        "layouts": [
            {
                "id": 14,
                "name": "Uthmani Hafs Layout",
                "total_pages": 604,
                "description": "Standard Uthmani script with Hafs recitation"
            }
        ]
    }

@router.get("/surah-names")
async def get_surah_names(db: aiosqlite.Connection = Depends(get_qul_db)):
    """Get all surah names"""
    cursor = await db.execute("""
        SELECT surah_number, name_arabic, name_english, total_ayahs
        FROM surah_names
        ORDER BY surah_number
    """)
    rows = await cursor.fetchall()
    
    surah_names = {}
    surah_list = []
    
    for row in rows:
        surah_data = {
            "surah_number": row[0],
            "name_arabic": row[1],
            "name_english": row[2],
            "total_ayahs": row[3]
        }
        surah_names[row[0]] = row[1]  # For quick lookup
        surah_list.append(surah_data)
    
    return {
        "surah_names": surah_names,
        "surahs": surah_list
    }

@router.get("/page/{page_number}")
async def get_qul_page(page_number: int, db: aiosqlite.Connection = Depends(get_qul_db)):
    """Get page data in QUL format with rendering logic"""
    
    # Get page layout data
    cursor = await db.execute("""
        SELECT page_number, line_number, line_type, is_centered, 
               first_word_id, last_word_id, surah_number
        FROM pages
        WHERE page_number = ?
        ORDER BY line_number
    """, (page_number,))
    
    page_lines = await cursor.fetchall()
    
    if not page_lines:
        raise HTTPException(status_code=404, detail=f"Page {page_number} not found")
    
    # Get all words for this page (optimization)
    word_ids = []
    for line in page_lines:
        if line[4] and line[5]:  # first_word_id and last_word_id
            word_ids.extend(range(line[4], line[5] + 1))
    
    if word_ids:
        placeholders = ','.join('?' * len(word_ids))
        cursor = await db.execute(f"""
            SELECT word_index, word_key, surah, ayah, text
            FROM words
            WHERE word_index IN ({placeholders})
            ORDER BY word_index
        """, word_ids)
        
        word_rows = await cursor.fetchall()
        word_data = {row[0]: row[4] for row in word_rows}  # word_index -> text
    else:
        word_data = {}
    
    # Get surah names
    cursor = await db.execute("""
        SELECT surah_number, name_arabic
        FROM surah_names
    """)
    surah_rows = await cursor.fetchall()
    surah_names = {row[0]: row[1] for row in surah_rows}
    
    # Build page content following QUL rendering logic
    page_content = []
    
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
        
        elif line_type == 'basmallah':
            # Render Bismillah
            line_content["content"] = "بِسۡمِ ٱللَّهِ ٱلرَّحۡمَٰنِ ٱلرَّحِيمِ"
        
        page_content.append(line_content)
    
    return {
        "page_number": page_number,
        "total_lines": len(page_content),
        "lines": page_content
    }

@router.get("/words/{first_word_id}/{last_word_id}")
async def get_words_range(
    first_word_id: int, 
    last_word_id: int, 
    db: aiosqlite.Connection = Depends(get_qul_db)
):
    """Get words in range (QUL helper function)"""
    
    cursor = await db.execute("""
        SELECT word_index, word_key, surah, ayah, text
        FROM words
        WHERE word_index >= ? AND word_index <= ?
        ORDER BY word_index
    """, (first_word_id, last_word_id))
    
    rows = await cursor.fetchall()
    
    words = []
    for row in rows:
        words.append({
            "word_index": row[0],
            "word_key": row[1],
            "surah": row[2],
            "ayah": row[3],
            "text": row[4]
        })
    
    return {
        "first_word_id": first_word_id,
        "last_word_id": last_word_id,
        "words": words,
        "combined_text": " ".join([w["text"] for w in words])
    }

@router.get("/surah/{surah_number}")
async def get_surah_info(surah_number: int, db: aiosqlite.Connection = Depends(get_qul_db)):
    """Get surah information"""
    
    cursor = await db.execute("""
        SELECT surah_number, name_arabic, name_english, total_ayahs
        FROM surah_names
        WHERE surah_number = ?
    """, (surah_number,))
    
    row = await cursor.fetchone()
    
    if not row:
        raise HTTPException(status_code=404, detail=f"Surah {surah_number} not found")
    
    return {
        "surah_number": row[0],
        "name_arabic": row[1],
        "name_english": row[2],
        "total_ayahs": row[3]
    }

@router.get("/ayah/{surah_number}/{ayah_number}")
async def get_ayah_words(
    surah_number: int, 
    ayah_number: int, 
    db: aiosqlite.Connection = Depends(get_qul_db)
):
    """Get all words for a specific ayah"""
    
    cursor = await db.execute("""
        SELECT word_index, word_key, surah, ayah, text
        FROM words
        WHERE surah = ? AND ayah = ?
        ORDER BY word_index
    """, (surah_number, ayah_number))
    
    rows = await cursor.fetchall()
    
    if not rows:
        raise HTTPException(
            status_code=404, 
            detail=f"Ayah {surah_number}:{ayah_number} not found"
        )
    
    words = []
    for row in rows:
        words.append({
            "word_index": row[0],
            "word_key": row[1],
            "surah": row[2],
            "ayah": row[3],
            "text": row[4]
        })
    
    return {
        "surah": surah_number,
        "ayah": ayah_number,
        "words": words,
        "text": " ".join([w["text"] for w in words])
    }

@router.get("/search")
async def search_quran_qul(q: str, limit: int = 20, db: aiosqlite.Connection = Depends(get_qul_db)):
    """Search Quran text in QUL format"""
    
    search_term = f"%{q.strip()}%"
    
    cursor = await db.execute("""
        SELECT word_index, word_key, surah, ayah, text
        FROM words
        WHERE text LIKE ?
        ORDER BY surah, ayah, word_index
        LIMIT ?
    """, (search_term, limit))
    
    rows = await cursor.fetchall()
    
    results = []
    for row in rows:
        results.append({
            "word_index": row[0],
            "word_key": row[1],
            "surah": row[2],
            "ayah": row[3],
            "text": row[4]
        })
    
    return {
        "query": q,
        "results_count": len(results),
        "results": results
    }