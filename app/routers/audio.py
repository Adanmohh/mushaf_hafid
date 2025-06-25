"""
Audio router - API endpoints for audio recitations and timing
"""

from fastapi import APIRouter, Depends, HTTPException
import aiosqlite
from app.database.connection import get_async_db

router = APIRouter()

@router.get("/recitations")
async def get_recitations(db: aiosqlite.Connection = Depends(get_async_db)):
    """Get all available recitations"""
    try:
        cursor = await db.execute("""
            SELECT id, reciter_name, style 
            FROM recitations
            ORDER BY reciter_name
        """)
        rows = await cursor.fetchall()
        
        recitations = []
        for row in rows:
            recitations.append({
                "id": row[0],
                "reciter_name": row[1],
                "style": row[2]
            })
        
        return {"recitations": recitations}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/word/{word_id}/recitation/{recitation_id}")
async def get_word_audio_timing(
    word_id: int,
    recitation_id: int,
    db: aiosqlite.Connection = Depends(get_async_db)
):
    """Get audio timing for a specific word and recitation"""
    try:
        cursor = await db.execute("""
            SELECT start_time, end_time, audio_file_url
            FROM audio_timings
            WHERE word_id = ? AND recitation_id = ?
        """, (word_id, recitation_id))
        row = await cursor.fetchone()
        
        if not row:
            raise HTTPException(
                status_code=404, 
                detail=f"Audio timing not found for word {word_id} and recitation {recitation_id}"
            )
        
        return {
            "word_id": word_id,
            "recitation_id": recitation_id,
            "start_time": row[0],
            "end_time": row[1],
            "duration": row[1] - row[0],
            "audio_url": row[2]
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/ayah/{surah_number}/{ayah_number}/recitation/{recitation_id}")
async def get_ayah_audio_timing(
    surah_number: int,
    ayah_number: int,
    recitation_id: int,
    db: aiosqlite.Connection = Depends(get_async_db)
):
    """Get audio timing for all words in an ayah"""
    try:
        cursor = await db.execute("""
            SELECT w.id, at.start_time, at.end_time, at.audio_file_url
            FROM words w
            JOIN audio_timings at ON w.id = at.word_id
            WHERE w.surah_number = ? AND w.ayah_number = ? AND at.recitation_id = ?
            ORDER BY w.word_position
        """, (surah_number, ayah_number, recitation_id))
        rows = await cursor.fetchall()
        
        if not rows:
            raise HTTPException(
                status_code=404, 
                detail=f"Audio timing not found for ayah {surah_number}:{ayah_number} and recitation {recitation_id}"
            )
        
        word_timings = []
        audio_url = rows[0][3]  # Assuming all words share the same audio file
        
        for row in rows:
            word_timings.append({
                "word_id": row[0],
                "start_time": row[1],
                "end_time": row[2]
            })
        
        return {
            "surah": surah_number,
            "ayah": ayah_number,
            "recitation_id": recitation_id,
            "audio_url": audio_url,
            "word_timings": word_timings
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")