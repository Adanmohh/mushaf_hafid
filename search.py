"""
Search router - API endpoints for searching Quranic text
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
import aiosqlite

from app.models.mushaf import SearchResult, SearchResponse
from app.database.connection import get_async_db

router = APIRouter()

@router.get("/", response_model=SearchResponse)
async def search_quran(
    q: str = Query(..., min_length=1, description="Search query"),
    search_type: str = Query("word", regex="^(word|ayah|surah)$", description="Search type: word, ayah, or surah"),
    layout_id: int = Query(1, description="Mushaf layout ID for page references"),
    limit: int = Query(50, ge=1, le=200, description="Maximum number of results"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    db: aiosqlite.Connection = Depends(get_async_db)
):
    """
    Search for words, ayahs, or surahs in the Quran
    
    Supports different search types:
    - word: Search for specific words in Arabic or translation
    - ayah: Search within ayah text
    - surah: Search within surah names
    """
    try:
        search_query = f"%{q}%"
        
        if search_type == "word":
            # Search for individual words
            cursor = await db.execute("""
                SELECT 
                    w.id, w.word_text_uthmani, w.surah_number, w.ayah_number,
                    wp.page_number, wp.line_number, w.translation_en,
                    (SELECT GROUP_CONCAT(w2.word_text_uthmani, ' ') 
                     FROM words w2 
                     WHERE w2.surah_number = w.surah_number AND w2.ayah_number = w.ayah_number
                     ORDER BY w2.word_position) as context
                FROM words w
                LEFT JOIN word_positions wp ON w.id = wp.word_id AND wp.mushaf_layout_id = ?
                WHERE w.word_text_uthmani LIKE ? 
                   OR w.translation_en LIKE ? 
                   OR w.transliteration_en LIKE ?
                ORDER BY w.surah_number, w.ayah_number, w.word_position
                LIMIT ? OFFSET ?
            """, (layout_id, search_query, search_query, search_query, limit, offset))
            
        elif search_type == "ayah":
            # Search within complete ayahs
            cursor = await db.execute("""
                SELECT DISTINCT
                    w.id, w.word_text_uthmani, w.surah_number, w.ayah_number,
                    wp.page_number, wp.line_number, w.translation_en,
                    (SELECT GROUP_CONCAT(w2.word_text_uthmani, ' ') 
                     FROM words w2 
                     WHERE w2.surah_number = w.surah_number AND w2.ayah_number = w.ayah_number
                     ORDER BY w2.word_position) as context
                FROM words w
                LEFT JOIN word_positions wp ON w.id = wp.word_id AND wp.mushaf_layout_id = ?
                WHERE w.surah_number IN (
                    SELECT DISTINCT w3.surah_number 
                    FROM words w3 
                    WHERE w3.word_text_uthmani LIKE ? 
                       OR w3.translation_en LIKE ?
                       OR w3.transliteration_en LIKE ?
                )
                AND w.ayah_number IN (
                    SELECT DISTINCT w4.ayah_number 
                    FROM words w4 
                    WHERE w4.surah_number = w.surah_number 
                      AND (w4.word_text_uthmani LIKE ? 
                           OR w4.translation_en LIKE ?
                           OR w4.transliteration_en LIKE ?)
                )
                ORDER BY w.surah_number, w.ayah_number, w.word_position
                LIMIT ? OFFSET ?
            """, (layout_id, search_query, search_query, search_query, 
                  search_query, search_query, search_query, limit, offset))
            
        else:  # surah search
            # Search for surahs (this would require a surahs table, for now search in words)
            cursor = await db.execute("""
                SELECT DISTINCT
                    w.id, w.word_text_uthmani, w.surah_number, w.ayah_number,
                    wp.page_number, wp.line_number, w.translation_en,
                    (SELECT GROUP_CONCAT(w2.word_text_uthmani, ' ') 
                     FROM words w2 
                     WHERE w2.surah_number = w.surah_number AND w2.ayah_number = w.ayah_number
                     ORDER BY w2.word_position) as context
                FROM words w
                LEFT JOIN word_positions wp ON w.id = wp.word_id AND wp.mushaf_layout_id = ?
                WHERE w.surah_number IN (
                    SELECT DISTINCT w3.surah_number 
                    FROM words w3 
                    WHERE w3.word_text_uthmani LIKE ? 
                       OR w3.translation_en LIKE ?
                       OR w3.transliteration_en LIKE ?
                )
                ORDER BY w.surah_number, w.ayah_number, w.word_position
                LIMIT ? OFFSET ?
            """, (layout_id, search_query, search_query, search_query, limit, offset))
        
        rows = await cursor.fetchall()
        
        # Get total count for pagination
        if search_type == "word":
            count_cursor = await db.execute("""
                SELECT COUNT(*)
                FROM words w
                WHERE w.word_text_uthmani LIKE ? 
                   OR w.translation_en LIKE ? 
                   OR w.transliteration_en LIKE ?
            """, (search_query, search_query, search_query))
        elif search_type == "ayah":
            count_cursor = await db.execute("""
                SELECT COUNT(DISTINCT w.surah_number || '-' || w.ayah_number)
                FROM words w
                WHERE w.word_text_uthmani LIKE ? 
                   OR w.translation_en LIKE ?
                   OR w.transliteration_en LIKE ?
            """, (search_query, search_query, search_query))
        else:  # surah
            count_cursor = await db.execute("""
                SELECT COUNT(DISTINCT w.surah_number)
                FROM words w
                WHERE w.word_text_uthmani LIKE ? 
                   OR w.translation_en LIKE ?
                   OR w.transliteration_en LIKE ?
            """, (search_query, search_query, search_query))
        
        total_count = (await count_cursor.fetchone())[0]
        
        # Build results
        results = []
        for row in rows:
            word_id, text, surah, ayah, page, line, translation, context = row
            
            results.append(SearchResult(
                word_id=word_id,
                text=text,
                surah=surah,
                ayah=ayah,
                page=page or 0,
                line=line or 0,
                translation=translation,
                context=context or text
            ))
        
        return SearchResponse(
            query=q,
            total_results=total_count,
            results=results
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search error: {str(e)}")

@router.get("/suggestions")
async def get_search_suggestions(
    q: str = Query(..., min_length=1, description="Partial search query"),
    limit: int = Query(10, ge=1, le=50, description="Maximum number of suggestions"),
    db: aiosqlite.Connection = Depends(get_async_db)
):
    """
    Get search suggestions based on partial input
    
    Returns suggested words and translations that match the partial query.
    """
    try:
        search_query = f"{q}%"  # Prefix matching
        
        # Get word suggestions
        cursor = await db.execute("""
            SELECT DISTINCT word_text_uthmani, translation_en, transliteration_en
            FROM words
            WHERE word_text_uthmani LIKE ? 
               OR translation_en LIKE ? 
               OR transliteration_en LIKE ?
            ORDER BY 
                CASE 
                    WHEN word_text_uthmani LIKE ? THEN 1
                    WHEN translation_en LIKE ? THEN 2
                    WHEN transliteration_en LIKE ? THEN 3
                    ELSE 4
                END,
                LENGTH(word_text_uthmani)
            LIMIT ?
        """, (search_query, search_query, search_query, 
              search_query, search_query, search_query, limit))
        
        rows = await cursor.fetchall()
        
        suggestions = []
        for row in rows:
            arabic, translation, transliteration = row
            
            suggestion = {
                "arabic": arabic,
                "translation": translation,
                "transliteration": transliteration
            }
            
            # Determine which field matched
            if arabic.startswith(q):
                suggestion["match_type"] = "arabic"
                suggestion["display"] = arabic
            elif translation and translation.lower().startswith(q.lower()):
                suggestion["match_type"] = "translation"
                suggestion["display"] = translation
            elif transliteration and transliteration.lower().startswith(q.lower()):
                suggestion["match_type"] = "transliteration"
                suggestion["display"] = transliteration
            else:
                suggestion["match_type"] = "partial"
                suggestion["display"] = arabic
            
            suggestions.append(suggestion)
        
        return {
            "query": q,
            "suggestions": suggestions
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Suggestions error: {str(e)}")

@router.get("/ayah/{surah_number}/{ayah_number}")
async def search_within_ayah(
    surah_number: int,
    ayah_number: int,
    q: str = Query(..., min_length=1, description="Search query within the ayah"),
    layout_id: int = Query(1, description="Mushaf layout ID"),
    db: aiosqlite.Connection = Depends(get_async_db)
):
    """
    Search for words within a specific ayah
    
    Returns all matching words within the specified ayah.
    """
    try:
        search_query = f"%{q}%"
        
        cursor = await db.execute("""
            SELECT 
                w.id, w.word_text_uthmani, w.word_position, w.translation_en, w.transliteration_en,
                wp.page_number, wp.line_number, wp.x_coordinate, wp.y_coordinate
            FROM words w
            LEFT JOIN word_positions wp ON w.id = wp.word_id AND wp.mushaf_layout_id = ?
            WHERE w.surah_number = ? AND w.ayah_number = ?
              AND (w.word_text_uthmani LIKE ? 
                   OR w.translation_en LIKE ? 
                   OR w.transliteration_en LIKE ?)
            ORDER BY w.word_position
        """, (layout_id, surah_number, ayah_number, search_query, search_query, search_query))
        
        rows = await cursor.fetchall()
        
        if not rows:
            return {
                "surah": surah_number,
                "ayah": ayah_number,
                "query": q,
                "matches": []
            }
        
        matches = []
        for row in rows:
            word_id, text, position, translation, transliteration, page, line, x, y = row
            
            matches.append({
                "word_id": word_id,
                "text": text,
                "position": position,
                "translation": translation,
                "transliteration": transliteration,
                "page": page,
                "line": line,
                "coordinates": {
                    "x": x,
                    "y": y
                } if x is not None and y is not None else None
            })
        
        return {
            "surah": surah_number,
            "ayah": ayah_number,
            "query": q,
            "total_matches": len(matches),
            "matches": matches
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ayah search error: {str(e)}")

@router.get("/advanced")
async def advanced_search(
    arabic: Optional[str] = Query(None, description="Arabic text search"),
    translation: Optional[str] = Query(None, description="Translation search"),
    transliteration: Optional[str] = Query(None, description="Transliteration search"),
    surah_start: Optional[int] = Query(None, ge=1, le=114, description="Start surah number"),
    surah_end: Optional[int] = Query(None, ge=1, le=114, description="End surah number"),
    layout_id: int = Query(1, description="Mushaf layout ID"),
    limit: int = Query(50, ge=1, le=200, description="Maximum number of results"),
    offset: int = Query(0, ge=0, description="Offset for pagination"),
    db: aiosqlite.Connection = Depends(get_async_db)
):
    """
    Advanced search with multiple criteria
    
    Allows searching with specific criteria for Arabic text, translation, 
    transliteration, and surah range.
    """
    try:
        # Build dynamic query
        conditions = []
        params = [layout_id]
        
        if arabic:
            conditions.append("w.word_text_uthmani LIKE ?")
            params.append(f"%{arabic}%")
        
        if translation:
            conditions.append("w.translation_en LIKE ?")
            params.append(f"%{translation}%")
        
        if transliteration:
            conditions.append("w.transliteration_en LIKE ?")
            params.append(f"%{transliteration}%")
        
        if surah_start:
            conditions.append("w.surah_number >= ?")
            params.append(surah_start)
        
        if surah_end:
            conditions.append("w.surah_number <= ?")
            params.append(surah_end)
        
        if not conditions:
            raise HTTPException(status_code=400, detail="At least one search criterion must be provided")
        
        where_clause = " AND ".join(conditions)
        
        # Main query
        query = f"""
            SELECT 
                w.id, w.word_text_uthmani, w.surah_number, w.ayah_number,
                wp.page_number, wp.line_number, w.translation_en,
                (SELECT GROUP_CONCAT(w2.word_text_uthmani, ' ') 
                 FROM words w2 
                 WHERE w2.surah_number = w.surah_number AND w2.ayah_number = w.ayah_number
                 ORDER BY w2.word_position) as context
            FROM words w
            LEFT JOIN word_positions wp ON w.id = wp.word_id AND wp.mushaf_layout_id = ?
            WHERE {where_clause}
            ORDER BY w.surah_number, w.ayah_number, w.word_position
            LIMIT ? OFFSET ?
        """
        
        params.extend([limit, offset])
        cursor = await db.execute(query, params)
        rows = await cursor.fetchall()
        
        # Count query
        count_query = f"""
            SELECT COUNT(*)
            FROM words w
            WHERE {where_clause}
        """
        count_cursor = await db.execute(count_query, params[1:-2])  # Exclude layout_id, limit, offset
        total_count = (await count_cursor.fetchone())[0]
        
        # Build results
        results = []
        for row in rows:
            word_id, text, surah, ayah, page, line, translation_text, context = row
            
            results.append(SearchResult(
                word_id=word_id,
                text=text,
                surah=surah,
                ayah=ayah,
                page=page or 0,
                line=line or 0,
                translation=translation_text,
                context=context or text
            ))
        
        return {
            "criteria": {
                "arabic": arabic,
                "translation": translation,
                "transliteration": transliteration,
                "surah_range": f"{surah_start or 1}-{surah_end or 114}"
            },
            "total_results": total_count,
            "results": results
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Advanced search error: {str(e)}")

