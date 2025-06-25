"""
Search router - API endpoints for searching Quranic text
"""

from fastapi import APIRouter, Depends, HTTPException, Query
import aiosqlite
from app.database.connection import get_async_db
from typing import List, Optional

router = APIRouter()

@router.get("/")
async def search_quran(
    q: str = Query(..., description="Search query"),
    limit: int = Query(20, description="Maximum number of results"),
    db: aiosqlite.Connection = Depends(get_async_db)
):
    """Search Quran text in Arabic, English translation, and transliteration"""
    try:
        search_term = f"%{q.strip()}%"
        
        cursor = await db.execute("""
            SELECT DISTINCT
                w.id, w.surah_number, w.ayah_number, w.word_text_uthmani,
                w.translation_en, w.transliteration_en,
                wp.page_number, wp.line_number
            FROM words w
            LEFT JOIN word_positions wp ON w.id = wp.word_id
            WHERE w.word_text_uthmani LIKE ? 
                OR w.translation_en LIKE ? 
                OR w.transliteration_en LIKE ?
            ORDER BY w.surah_number, w.ayah_number, w.word_position
            LIMIT ?
        """, (search_term, search_term, search_term, limit))
        
        rows = await cursor.fetchall()
        
        results = []
        for row in rows:
            results.append({
                "word_id": row[0],
                "surah": row[1],
                "ayah": row[2],
                "text": row[3],
                "translation": row[4],
                "transliteration": row[5],
                "page": row[6],
                "line": row[7]
            })
        
        return {
            "query": q,
            "results_count": len(results),
            "results": results
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/suggestions")
async def get_search_suggestions(
    q: str = Query(..., description="Search query for suggestions"),
    limit: int = Query(10, description="Maximum number of suggestions"),
    db: aiosqlite.Connection = Depends(get_async_db)
):
    """Get search suggestions based on partial query"""
    try:
        search_term = f"{q.strip()}%"
        
        cursor = await db.execute("""
            SELECT DISTINCT translation_en
            FROM words
            WHERE translation_en LIKE ?
            ORDER BY translation_en
            LIMIT ?
        """, (search_term, limit))
        
        rows = await cursor.fetchall()
        
        suggestions = [row[0] for row in rows if row[0]]
        
        return {
            "query": q,
            "suggestions": suggestions
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/advanced")
async def advanced_search(
    arabic: Optional[str] = Query(None, description="Arabic text search"),
    translation: Optional[str] = Query(None, description="English translation search"),
    transliteration: Optional[str] = Query(None, description="Transliteration search"),
    surah: Optional[int] = Query(None, description="Specific surah number"),
    ayah: Optional[int] = Query(None, description="Specific ayah number"),
    limit: int = Query(20, description="Maximum number of results"),
    db: aiosqlite.Connection = Depends(get_async_db)
):
    """Advanced search with multiple filters"""
    try:
        conditions = []
        params = []
        
        if arabic:
            conditions.append("w.word_text_uthmani LIKE ?")
            params.append(f"%{arabic}%")
        
        if translation:
            conditions.append("w.translation_en LIKE ?")
            params.append(f"%{translation}%")
        
        if transliteration:
            conditions.append("w.transliteration_en LIKE ?")
            params.append(f"%{transliteration}%")
        
        if surah:
            conditions.append("w.surah_number = ?")
            params.append(surah)
        
        if ayah:
            conditions.append("w.ayah_number = ?")
            params.append(ayah)
        
        if not conditions:
            raise HTTPException(status_code=400, detail="At least one search parameter is required")
        
        where_clause = " AND ".join(conditions)
        params.append(limit)
        
        query = f"""
            SELECT DISTINCT
                w.id, w.surah_number, w.ayah_number, w.word_text_uthmani,
                w.translation_en, w.transliteration_en,
                wp.page_number, wp.line_number
            FROM words w
            LEFT JOIN word_positions wp ON w.id = wp.word_id
            WHERE {where_clause}
            ORDER BY w.surah_number, w.ayah_number, w.word_position
            LIMIT ?
        """
        
        cursor = await db.execute(query, params)
        rows = await cursor.fetchall()
        
        results = []
        for row in rows:
            results.append({
                "word_id": row[0],
                "surah": row[1],
                "ayah": row[2],
                "text": row[3],
                "translation": row[4],
                "transliteration": row[5],
                "page": row[6],
                "line": row[7]
            })
        
        return {
            "filters": {
                "arabic": arabic,
                "translation": translation,
                "transliteration": transliteration,
                "surah": surah,
                "ayah": ayah
            },
            "results_count": len(results),
            "results": results
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")