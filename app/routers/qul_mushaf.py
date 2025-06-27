"""
QUL-compatible Mushaf router following QUL rendering logic
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import List, Dict, Any, Optional
import sqlite3
import os

router = APIRouter(prefix="/qul", tags=["QUL Mushaf"])

# Database path
QUL_DB_PATH = "app/database/qul_complete.db"

def get_qul_connection():
    """Get connection to QUL database"""
    if not os.path.exists(QUL_DB_PATH):
        raise HTTPException(status_code=500, detail="QUL database not found")
    return sqlite3.connect(QUL_DB_PATH)

@router.get("/layouts")
async def get_layouts():
    """Get available QUL layouts"""
    try:
        conn = get_qul_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM layout_info")
        layouts = cursor.fetchall()
        conn.close()
        
        layout_list = []
        for layout in layouts:
            layout_list.append({
                "name": layout[0],
                "number_of_pages": layout[1],
                "lines_per_page": layout[2],
                "font_name": layout[3]
            })
        
        return {"layouts": layout_list}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching layouts: {str(e)}")

@router.get("/page/{page_number}")
async def get_page(page_number: int):
    """Get QUL page data with proper rendering structure"""
    try:
        if page_number < 1 or page_number > 604:
            raise HTTPException(status_code=400, detail="Page number must be between 1 and 604")
        
        conn = get_qul_connection()
        cursor = conn.cursor()
        
        # Get page lines
        cursor.execute('''
            SELECT line_number, line_type, is_centered, first_word_id, last_word_id, surah_number
            FROM pages 
            WHERE page_number = ? 
            ORDER BY line_number
        ''', (page_number,))
        
        page_lines = cursor.fetchall()
        
        if not page_lines:
            raise HTTPException(status_code=404, detail=f"Page {page_number} not found")
        
        # Process each line according to QUL rendering logic
        lines = []
        for line_data in page_lines:
            line_number, line_type, is_centered, first_word_id, last_word_id, surah_number = line_data
            
            line = {
                "line_number": line_number,
                "line_type": line_type,
                "is_centered": bool(is_centered),
                "words": [],
                "content": "",
                "first_word_id": first_word_id,
                "last_word_id": last_word_id,
                "surah_number": surah_number
            }
            
            if line_type == "surah_name":
                # Get surah name
                if surah_number:
                    cursor.execute("SELECT name_arabic FROM chapters WHERE id = ?", (surah_number,))
                    surah_result = cursor.fetchone()
                    if surah_result:
                        line["content"] = f"سورة {surah_result[0]}"
                        line["words"] = [{"word_id": 0, "text": line["content"]}]
            
            elif line_type == "basmallah":
                line["content"] = "بِسۡمِ ٱللَّهِ ٱلرَّحۡمَٰنِ ٱلرَّحِيمِ"
                line["words"] = [{"word_id": 0, "text": line["content"]}]
            
            elif line_type == "ayah":
                # Get words for this line
                if first_word_id and last_word_id:
                    cursor.execute('''
                        SELECT id, text FROM words 
                        WHERE id BETWEEN ? AND ?
                        ORDER BY id
                    ''', (first_word_id, last_word_id))
                    
                    word_results = cursor.fetchall()
                    words = []
                    word_texts = []
                    
                    for word_id, text in word_results:
                        words.append({"word_id": word_id, "text": text})
                        word_texts.append(text)
                    
                    line["words"] = words
                    line["content"] = " ".join(word_texts)
            
            lines.append(line)
        
        conn.close()
        
        # Get page-specific font info
        font_file = f"p{page_number}.woff"
        
        return {
            "page_number": page_number,
            "total_lines": len(lines),
            "lines": lines,
            "font_file": font_file,
            "font_path": f"/static/fonts/{font_file}"
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching page: {str(e)}")

@router.get("/surah-names")
async def get_surah_names():
    """Get all surah names"""
    try:
        conn = get_qul_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, name_simple, name_arabic, verses_count FROM chapters ORDER BY id")
        chapters = cursor.fetchall()
        conn.close()
        
        surah_names = {}
        surahs = []
        
        for chapter in chapters:
            chapter_id, name_simple, name_arabic, verses_count = chapter
            surah_names[chapter_id] = name_arabic
            surahs.append({
                "id": chapter_id,
                "name_simple": name_simple,
                "name_arabic": name_arabic,
                "verses_count": verses_count
            })
        
        return {"surah_names": surah_names, "surahs": surahs}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching surah names: {str(e)}")

@router.get("/search")
async def search_quran(
    query: str = Query(..., min_length=1),
    limit: int = Query(default=20, ge=1, le=100)
):
    """Search in the Quran text"""
    try:
        conn = get_qul_connection()
        cursor = conn.cursor()
        
        # Search in Arabic text
        cursor.execute('''
            SELECT w.id, w.location, w.surah, w.ayah, w.text,
                   c.name_simple, c.name_arabic
            FROM words w
            JOIN chapters c ON w.surah = c.id
            WHERE w.text LIKE ?
            ORDER BY w.surah, w.ayah, w.id
            LIMIT ?
        ''', (f'%{query}%', limit))
        
        results = cursor.fetchall()
        
        search_results = []
        for result in results:
            word_id, location, surah, ayah, text, surah_name, surah_arabic = result
            
            # Find which page this word is on
            cursor.execute('''
                SELECT page_number FROM pages 
                WHERE first_word_id <= ? AND last_word_id >= ?
                LIMIT 1
            ''', (word_id, word_id))
            
            page_result = cursor.fetchone()
            page_number = page_result[0] if page_result else None
            
            search_results.append({
                "word_id": word_id,
                "word_key": location,
                "surah": surah,
                "ayah": ayah,
                "text": text,
                "surah_name": surah_name,
                "surah_arabic": surah_arabic,
                "page": page_number
            })
        
        conn.close()
        
        return {
            "results": search_results,
            "total_found": len(search_results),
            "query": query
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching: {str(e)}")

@router.get("/ayah/{surah_number}/{ayah_number}")
async def get_ayah(surah_number: int, ayah_number: int):
    """Get specific ayah and find which page it's on"""
    try:
        if surah_number < 1 or surah_number > 114:
            raise HTTPException(status_code=400, detail="Surah number must be between 1 and 114")
        
        conn = get_qul_connection()
        cursor = conn.cursor()
        
        # Get ayah words
        cursor.execute('''
            SELECT id, text FROM words 
            WHERE surah = ? AND ayah = ?
            ORDER BY word
        ''', (surah_number, ayah_number))
        
        words = cursor.fetchall()
        
        if not words:
            raise HTTPException(status_code=404, detail=f"Ayah {surah_number}:{ayah_number} not found")
        
        # Find page containing this ayah
        first_word_id = words[0][0]
        cursor.execute('''
            SELECT page_number FROM pages 
            WHERE first_word_id <= ? AND last_word_id >= ?
            LIMIT 1
        ''', (first_word_id, first_word_id))
        
        page_result = cursor.fetchone()
        page_number = page_result[0] if page_result else None
        
        # Get surah info
        cursor.execute("SELECT name_simple, name_arabic FROM chapters WHERE id = ?", (surah_number,))
        surah_info = cursor.fetchone()
        
        conn.close()
        
        ayah_text = " ".join([word[1] for word in words])
        
        return {
            "surah_number": surah_number,
            "ayah_number": ayah_number,
            "text": ayah_text,
            "words": [{"word_id": w[0], "text": w[1]} for w in words],
            "page_number": page_number,
            "surah_name": surah_info[0] if surah_info else None,
            "surah_arabic": surah_info[1] if surah_info else None
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching ayah: {str(e)}")

@router.get("/stats")
async def get_quran_stats():
    """Get Quran statistics"""
    try:
        conn = get_qul_connection()
        cursor = conn.cursor()
        
        # Get total counts
        cursor.execute("SELECT COUNT(*) FROM words")
        total_words = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(DISTINCT page_number) FROM pages")
        total_pages = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM chapters")
        total_surahs = cursor.fetchone()[0]
        
        # Get total ayahs
        cursor.execute("SELECT SUM(verses_count) FROM chapters")
        total_ayahs = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "total_words": total_words,
            "total_pages": total_pages,
            "total_surahs": total_surahs,
            "total_ayahs": total_ayahs,
            "layout_name": "QPC HAFS Complete",
            "font_system": "Page-specific WOFF fonts"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching stats: {str(e)}")