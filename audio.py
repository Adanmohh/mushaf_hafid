"""
Audio router - API endpoints for audio recitations and word-level timing
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse
from typing import List, Optional
import aiosqlite
import os

from app.models.mushaf import (
    Recitation, RecitationsResponse, AudioTiming, AyahAudio
)
from app.database.connection import get_async_db

router = APIRouter()

@router.get("/recitations", response_model=RecitationsResponse)
async def get_recitations(db: aiosqlite.Connection = Depends(get_async_db)):
    """
    Get all available recitations
    
    Returns a list of all available reciters and their recitation styles.
    """
    try:
        cursor = await db.execute("""
            SELECT id, reciter_name, style 
            FROM recitations
            ORDER BY reciter_name
        """)
        rows = await cursor.fetchall()
        
        recitations = []
        for row in rows:
            recitations.append(Recitation(
                id=row[0],
                reciter_name=row[1],
                style=row[2]
            ))
        
        return RecitationsResponse(recitations=recitations)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/recitation/{recitation_id}", response_model=Recitation)
async def get_recitation(
    recitation_id: int,
    db: aiosqlite.Connection = Depends(get_async_db)
):
    """
    Get specific recitation by ID
    
    Returns detailed information about a specific reciter.
    """
    try:
        cursor = await db.execute("""
            SELECT id, reciter_name, style 
            FROM recitations 
            WHERE id = ?
        """, (recitation_id,))
        row = await cursor.fetchone()
        
        if not row:
            raise HTTPException(status_code=404, detail=f"Recitation {recitation_id} not found")
        
        return Recitation(
            id=row[0],
            reciter_name=row[1],
            style=row[2]
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/word/{word_id}/recitation/{recitation_id}", response_model=AudioTiming)
async def get_word_audio_timing(
    word_id: int,
    recitation_id: int,
    db: aiosqlite.Connection = Depends(get_async_db)
):
    """
    Get audio timing for a specific word by a specific reciter
    
    Returns precise start and end times for word-level audio synchronization.
    """
    try:
        cursor = await db.execute("""
            SELECT word_id, recitation_id, start_time, end_time, audio_file_url
            FROM audio_timings
            WHERE word_id = ? AND recitation_id = ?
        """, (word_id, recitation_id))
        row = await cursor.fetchone()
        
        if not row:
            raise HTTPException(
                status_code=404, 
                detail=f"Audio timing not found for word {word_id} with recitation {recitation_id}"
            )
        
        return AudioTiming(
            word_id=row[0],
            recitation_id=row[1],
            start_time=row[2],
            end_time=row[3],
            audio_url=row[4]
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/ayah/{surah_number}/{ayah_number}/recitation/{recitation_id}", response_model=AyahAudio)
async def get_ayah_audio(
    surah_number: int,
    ayah_number: int,
    recitation_id: int,
    db: aiosqlite.Connection = Depends(get_async_db)
):
    """
    Get complete ayah audio with word-level timings
    
    Returns the audio file URL and precise timing for each word in the ayah.
    """
    try:
        # Verify recitation exists
        cursor = await db.execute("""
            SELECT id FROM recitations WHERE id = ?
        """, (recitation_id,))
        if not await cursor.fetchone():
            raise HTTPException(status_code=404, detail=f"Recitation {recitation_id} not found")
        
        # Get all words and their timings for the ayah
        cursor = await db.execute("""
            SELECT 
                w.id, w.word_text_uthmani, w.word_position,
                at.start_time, at.end_time, at.audio_file_url
            FROM words w
            LEFT JOIN audio_timings at ON w.id = at.word_id AND at.recitation_id = ?
            WHERE w.surah_number = ? AND w.ayah_number = ?
            ORDER BY w.word_position
        """, (recitation_id, surah_number, ayah_number))
        rows = await cursor.fetchall()
        
        if not rows:
            raise HTTPException(
                status_code=404, 
                detail=f"Ayah {surah_number}:{ayah_number} not found"
            )
        
        word_timings = []
        audio_url = None
        
        for row in rows:
            word_id, text, position, start_time, end_time, file_url = row
            
            if start_time is not None and end_time is not None:
                word_timings.append(AudioTiming(
                    word_id=word_id,
                    recitation_id=recitation_id,
                    start_time=start_time,
                    end_time=end_time,
                    audio_url=file_url
                ))
                
                # Use the first audio file URL as the ayah audio URL
                if audio_url is None:
                    audio_url = file_url
        
        if not word_timings:
            raise HTTPException(
                status_code=404, 
                detail=f"No audio timings found for ayah {surah_number}:{ayah_number} with recitation {recitation_id}"
            )
        
        return AyahAudio(
            surah=surah_number,
            ayah=ayah_number,
            recitation_id=recitation_id,
            audio_url=audio_url,
            word_timings=word_timings
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/file/{audio_filename}")
async def get_audio_file(audio_filename: str):
    """
    Serve audio files
    
    Returns the actual audio file for playback.
    """
    try:
        # Construct the full path to the audio file
        audio_path = os.path.join("static", "audio", audio_filename)
        
        # Check if file exists
        if not os.path.exists(audio_path):
            raise HTTPException(status_code=404, detail=f"Audio file {audio_filename} not found")
        
        # Return the file
        return FileResponse(
            path=audio_path,
            media_type="audio/mpeg",
            filename=audio_filename
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File error: {str(e)}")

@router.get("/surah/{surah_number}/recitation/{recitation_id}/timings")
async def get_surah_timings(
    surah_number: int,
    recitation_id: int,
    db: aiosqlite.Connection = Depends(get_async_db)
):
    """
    Get all word timings for a complete surah
    
    Useful for preloading timing data for an entire surah.
    """
    try:
        cursor = await db.execute("""
            SELECT 
                w.id, w.ayah_number, w.word_position, w.word_text_uthmani,
                at.start_time, at.end_time, at.audio_file_url
            FROM words w
            JOIN audio_timings at ON w.id = at.word_id
            WHERE w.surah_number = ? AND at.recitation_id = ?
            ORDER BY w.ayah_number, w.word_position
        """, (surah_number, recitation_id))
        rows = await cursor.fetchall()
        
        if not rows:
            raise HTTPException(
                status_code=404, 
                detail=f"No audio timings found for surah {surah_number} with recitation {recitation_id}"
            )
        
        # Group by ayah
        ayahs = {}
        for row in rows:
            word_id, ayah_num, word_pos, text, start_time, end_time, audio_url = row
            
            if ayah_num not in ayahs:
                ayahs[ayah_num] = {
                    "ayah_number": ayah_num,
                    "words": []
                }
            
            ayahs[ayah_num]["words"].append({
                "word_id": word_id,
                "position": word_pos,
                "text": text,
                "start_time": start_time,
                "end_time": end_time,
                "duration": end_time - start_time,
                "audio_url": audio_url
            })
        
        return {
            "surah_number": surah_number,
            "recitation_id": recitation_id,
            "total_ayahs": len(ayahs),
            "ayahs": list(ayahs.values())
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/stats/recitation/{recitation_id}")
async def get_recitation_stats(
    recitation_id: int,
    db: aiosqlite.Connection = Depends(get_async_db)
):
    """
    Get statistics for a specific recitation
    
    Returns information about coverage and timing statistics.
    """
    try:
        # Verify recitation exists
        cursor = await db.execute("""
            SELECT reciter_name, style FROM recitations WHERE id = ?
        """, (recitation_id,))
        recitation_row = await cursor.fetchone()
        
        if not recitation_row:
            raise HTTPException(status_code=404, detail=f"Recitation {recitation_id} not found")
        
        # Get timing statistics
        cursor = await db.execute("""
            SELECT 
                COUNT(*) as total_words,
                AVG(end_time - start_time) as avg_duration,
                MIN(end_time - start_time) as min_duration,
                MAX(end_time - start_time) as max_duration,
                COUNT(DISTINCT w.surah_number) as surahs_covered,
                COUNT(DISTINCT w.surah_number || '-' || w.ayah_number) as ayahs_covered
            FROM audio_timings at
            JOIN words w ON at.word_id = w.id
            WHERE at.recitation_id = ?
        """, (recitation_id,))
        stats_row = await cursor.fetchone()
        
        return {
            "recitation_id": recitation_id,
            "reciter_name": recitation_row[0],
            "style": recitation_row[1],
            "statistics": {
                "total_words": stats_row[0],
                "average_word_duration_ms": round(stats_row[1], 2) if stats_row[1] else 0,
                "min_word_duration_ms": stats_row[2] or 0,
                "max_word_duration_ms": stats_row[3] or 0,
                "surahs_covered": stats_row[4],
                "ayahs_covered": stats_row[5]
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

