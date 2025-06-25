"""
Mushaf router - API endpoints for Mushaf layouts and pages
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
import aiosqlite

from app.models.mushaf import (
    MushafLayout, LayoutsResponse, Page, PageResponse, 
    Word, WordPosition, Line, ErrorResponse
)
from app.database.connection import get_async_db

router = APIRouter()

@router.get("/layouts", response_model=LayoutsResponse)
async def get_mushaf_layouts(db: aiosqlite.Connection = Depends(get_async_db)):
    """
    Get all available Mushaf layouts
    
    Returns a list of all available Mushaf layouts with their specifications.
    """
    try:
        cursor = await db.execute("""
            SELECT id, name, total_pages, lines_per_page, font_name 
            FROM mushaf_layouts
            ORDER BY id
        """)
        rows = await cursor.fetchall()
        
        layouts = []
        for row in rows:
            layouts.append(MushafLayout(
                id=row[0],
                name=row[1],
                total_pages=row[2],
                lines_per_page=row[3],
                font_name=row[4]
            ))
        
        return LayoutsResponse(layouts=layouts)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/layout/{layout_id}", response_model=MushafLayout)
async def get_mushaf_layout(
    layout_id: int,
    db: aiosqlite.Connection = Depends(get_async_db)
):
    """
    Get specific Mushaf layout by ID
    
    Returns detailed information about a specific Mushaf layout.
    """
    try:
        cursor = await db.execute("""
            SELECT id, name, total_pages, lines_per_page, font_name 
            FROM mushaf_layouts 
            WHERE id = ?
        """, (layout_id,))
        row = await cursor.fetchone()
        
        if not row:
            raise HTTPException(status_code=404, detail=f"Mushaf layout {layout_id} not found")
        
        return MushafLayout(
            id=row[0],
            name=row[1],
            total_pages=row[2],
            lines_per_page=row[3],
            font_name=row[4]
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/layout/{layout_id}/page/{page_number}", response_model=PageResponse)
async def get_mushaf_page(
    layout_id: int,
    page_number: int,
    db: aiosqlite.Connection = Depends(get_async_db)
):
    """
    Get complete page data for a specific Mushaf layout and page number
    
    Returns all words, their positions, and line organization for the specified page.
    """
    try:
        # Verify layout exists
        cursor = await db.execute("""
            SELECT id FROM mushaf_layouts WHERE id = ?
        """, (layout_id,))
        if not await cursor.fetchone():
            raise HTTPException(status_code=404, detail=f"Mushaf layout {layout_id} not found")
        
        # Get page information
        cursor = await db.execute("""
            SELECT id, page_number, image_url 
            FROM pages 
            WHERE mushaf_layout_id = ? AND page_number = ?
        """, (layout_id, page_number))
        page_row = await cursor.fetchone()
        
        if not page_row:
            raise HTTPException(
                status_code=404, 
                detail=f"Page {page_number} not found for layout {layout_id}"
            )
        
        page_id = page_row[0]
        image_url = page_row[2]
        
        # Get all lines for this page
        cursor = await db.execute("""
            SELECT id, line_number 
            FROM lines 
            WHERE page_id = ? 
            ORDER BY line_number
        """, (page_id,))
        line_rows = await cursor.fetchall()
        
        lines = []
        for line_row in line_rows:
            line_id, line_number = line_row
            
            # Get all words for this line with their positions
            cursor = await db.execute("""
                SELECT 
                    w.id, w.word_position, w.surah_number, w.ayah_number,
                    w.word_text_uthmani, w.translation_en, w.transliteration_en,
                    wp.x_coordinate, wp.y_coordinate, wp.width, wp.height
                FROM words w
                LEFT JOIN word_positions wp ON w.id = wp.word_id 
                    AND wp.mushaf_layout_id = ? AND wp.page_number = ?
                WHERE w.line_id = ?
                ORDER BY w.word_position
            """, (layout_id, page_number, line_id))
            word_rows = await cursor.fetchall()
            
            words = []
            for word_row in word_rows:
                word_id, word_pos, surah, ayah, text, translation, transliteration, x, y, w, h = word_row
                
                # Create word position (default to 0,0 if not found)
                position = WordPosition(
                    x=x or 0,
                    y=y or 0,
                    width=w or 0,
                    height=h or 0
                )
                
                word = Word(
                    id=word_id,
                    text=text,
                    surah=surah,
                    ayah=ayah,
                    position=position,
                    translation=translation,
                    transliteration=transliteration
                )
                words.append(word)
            
            if words:  # Only add lines that have words
                line = Line(line_number=line_number, words=words)
                lines.append(line)
        
        page = Page(
            page_number=page_number,
            layout_id=layout_id,
            image_url=image_url,
            lines=lines
        )
        
        return PageResponse(page=page)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/surah/{surah_number}/ayah/{ayah_number}/page")
async def get_ayah_page_location(
    surah_number: int,
    ayah_number: int,
    layout_id: int = Query(1, description="Mushaf layout ID"),
    db: aiosqlite.Connection = Depends(get_async_db)
):
    """
    Find which page and line contains a specific ayah
    
    Useful for navigation to specific ayahs.
    """
    try:
        cursor = await db.execute("""
            SELECT DISTINCT wp.page_number, wp.line_number
            FROM words w
            JOIN word_positions wp ON w.id = wp.word_id
            WHERE w.surah_number = ? AND w.ayah_number = ? 
                AND wp.mushaf_layout_id = ?
            ORDER BY wp.page_number, wp.line_number
            LIMIT 1
        """, (surah_number, ayah_number, layout_id))
        
        result = await cursor.fetchone()
        
        if not result:
            raise HTTPException(
                status_code=404, 
                detail=f"Ayah {surah_number}:{ayah_number} not found in layout {layout_id}"
            )
        
        return {
            "surah": surah_number,
            "ayah": ayah_number,
            "layout_id": layout_id,
            "page_number": result[0],
            "line_number": result[1]
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")