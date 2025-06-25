# Quranic Mushaf View - Implementation Plan

## Overview

This document outlines the step-by-step implementation plan for creating a Quranic Mushaf view with FastAPI backend, based on research from QUL (Quranic Universal Library), Quran.com, open-mushaf project, and quran-align project.

## Phase 1: Data Preparation and Database Setup

### 1.1. Data Sources

Based on our research, we will use the following data sources:

1. **Mushaf Layout Data**: From QUL's Uthmani Hafs layout (SQLite format)
   - 604 pages, 15 lines per page
   - Word-level positioning coordinates
   - Precise layout matching printed Mushaf

2. **Audio Data**: From EveryAyah or QUL's recitation resources
   - High-quality MP3 files
   - Segmented by ayah or surah

3. **Word Timing Data**: From quran-align project
   - Word-precise timestamps
   - Start and end times for each word
   - Compatible with EveryAyah audio format

4. **Text Data**: From QUL or Tanzil project
   - Uthmani script text
   - Word-by-word translations
   - Transliterations

### 1.2. Database Schema Implementation

```sql
-- Create tables based on our schema design
CREATE TABLE mushaf_layouts (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    total_pages INTEGER NOT NULL,
    lines_per_page INTEGER NOT NULL,
    font_name TEXT NOT NULL
);

CREATE TABLE pages (
    id INTEGER PRIMARY KEY,
    mushaf_layout_id INTEGER NOT NULL,
    page_number INTEGER NOT NULL,
    image_url TEXT,
    FOREIGN KEY (mushaf_layout_id) REFERENCES mushaf_layouts(id)
);

CREATE TABLE lines (
    id INTEGER PRIMARY KEY,
    page_id INTEGER NOT NULL,
    line_number INTEGER NOT NULL,
    FOREIGN KEY (page_id) REFERENCES pages(id)
);

CREATE TABLE words (
    id INTEGER PRIMARY KEY,
    line_id INTEGER NOT NULL,
    word_position INTEGER NOT NULL,
    surah_number INTEGER NOT NULL,
    ayah_number INTEGER NOT NULL,
    word_text_uthmani TEXT NOT NULL,
    translation_en TEXT,
    transliteration_en TEXT,
    FOREIGN KEY (line_id) REFERENCES lines(id)
);

CREATE TABLE word_positions (
    id INTEGER PRIMARY KEY,
    word_id INTEGER NOT NULL,
    mushaf_layout_id INTEGER NOT NULL,
    page_number INTEGER NOT NULL,
    line_number INTEGER NOT NULL,
    x_coordinate INTEGER NOT NULL,
    y_coordinate INTEGER NOT NULL,
    width INTEGER NOT NULL,
    height INTEGER NOT NULL,
    FOREIGN KEY (word_id) REFERENCES words(id),
    FOREIGN KEY (mushaf_layout_id) REFERENCES mushaf_layouts(id)
);

CREATE TABLE recitations (
    id INTEGER PRIMARY KEY,
    reciter_name TEXT NOT NULL,
    style TEXT NOT NULL
);

CREATE TABLE audio_timings (
    id INTEGER PRIMARY KEY,
    word_id INTEGER NOT NULL,
    recitation_id INTEGER NOT NULL,
    start_time INTEGER NOT NULL,
    end_time INTEGER NOT NULL,
    audio_file_url TEXT NOT NULL,
    FOREIGN KEY (word_id) REFERENCES words(id),
    FOREIGN KEY (recitation_id) REFERENCES recitations(id)
);
```

## Phase 2: FastAPI Backend Development

### 2.1. Project Structure

```
quran_mushaf_api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── mushaf.py
│   │   ├── audio.py
│   │   └── database.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── mushaf.py
│   │   ├── audio.py
│   │   └── search.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── mushaf_service.py
│   │   └── audio_service.py
│   └── database/
│       ├── __init__.py
│       ├── connection.py
│       └── quran.db
├── static/
│   ├── audio/
│   └── images/
├── requirements.txt
└── README.md
```

### 2.2. Core API Endpoints

#### 2.2.1. Mushaf Layout Endpoints

```python
# GET /api/v1/mushaf/layouts
# Response: List of available Mushaf layouts
{
    "layouts": [
        {
            "id": 1,
            "name": "Uthmani Hafs",
            "total_pages": 604,
            "lines_per_page": 15,
            "font_name": "me_quran"
        }
    ]
}

# GET /api/v1/mushaf/layout/{layout_id}/page/{page_number}
# Response: Complete page data with word positions
{
    "page": {
        "page_number": 1,
        "layout_id": 1,
        "image_url": "/static/images/page_001.png",
        "lines": [
            {
                "line_number": 1,
                "words": [
                    {
                        "id": 1,
                        "text": "بِسْمِ",
                        "surah": 1,
                        "ayah": 1,
                        "position": {
                            "x": 100,
                            "y": 50,
                            "width": 40,
                            "height": 20
                        },
                        "translation": "In the name",
                        "transliteration": "Bismi"
                    }
                ]
            }
        ]
    }
}
```

#### 2.2.2. Audio Endpoints

```python
# GET /api/v1/recitations
# Response: List of available reciters
{
    "recitations": [
        {
            "id": 1,
            "reciter_name": "Abdul Basit Abdul Samad",
            "style": "Murattal"
        }
    ]
}

# GET /api/v1/audio/word/{word_id}/recitation/{recitation_id}
# Response: Audio timing and file information
{
    "word_id": 1,
    "recitation_id": 1,
    "start_time": 1500,
    "end_time": 2200,
    "audio_url": "/static/audio/001001_abdul_basit.mp3",
    "duration": 700
}

# GET /api/v1/audio/ayah/{surah_number}/{ayah_number}/recitation/{recitation_id}
# Response: Complete ayah audio with word timings
{
    "surah": 1,
    "ayah": 1,
    "recitation_id": 1,
    "audio_url": "/static/audio/001001_abdul_basit.mp3",
    "word_timings": [
        {
            "word_id": 1,
            "start_time": 1500,
            "end_time": 2200,
            "text": "بِسْمِ"
        }
    ]
}
```

#### 2.2.3. Search Endpoints

```python
# GET /api/v1/search?q={query}&type={word|ayah|surah}
# Response: Search results with page references
{
    "query": "الله",
    "results": [
        {
            "word_id": 2,
            "text": "اللَّهِ",
            "surah": 1,
            "ayah": 1,
            "page": 1,
            "line": 1,
            "translation": "Allah",
            "context": "بِسْمِ اللَّهِ الرَّحْمَـٰنِ الرَّحِيمِ"
        }
    ]
}
```

### 2.3. Data Models (Pydantic)

```python
from pydantic import BaseModel
from typing import List, Optional

class WordPosition(BaseModel):
    x: int
    y: int
    width: int
    height: int

class Word(BaseModel):
    id: int
    text: str
    surah: int
    ayah: int
    position: WordPosition
    translation: Optional[str] = None
    transliteration: Optional[str] = None

class Line(BaseModel):
    line_number: int
    words: List[Word]

class Page(BaseModel):
    page_number: int
    layout_id: int
    image_url: Optional[str] = None
    lines: List[Line]

class MushafLayout(BaseModel):
    id: int
    name: str
    total_pages: int
    lines_per_page: int
    font_name: str

class AudioTiming(BaseModel):
    word_id: int
    recitation_id: int
    start_time: int
    end_time: int
    audio_url: str
    duration: int

class Recitation(BaseModel):
    id: int
    reciter_name: str
    style: str
```

## Phase 3: Frontend Integration Considerations

### 3.1. Word-Level Interaction

The frontend should be able to:

1. **Display Mushaf Pages**: Render pages with precise word positioning
2. **Word Highlighting**: Highlight words during audio playback
3. **Click Interactions**: Allow users to click on words for translations/audio
4. **Audio Synchronization**: Sync audio playback with word highlighting
5. **Navigation**: Navigate between pages, surahs, and ayahs

### 3.2. Responsive Design

- **Desktop**: Full page view with side panels for controls
- **Mobile**: Optimized layout with touch-friendly controls
- **Tablet**: Hybrid approach with collapsible panels

### 3.3. Performance Optimization

- **Lazy Loading**: Load pages and audio on demand
- **Caching**: Cache frequently accessed pages and audio
- **Progressive Loading**: Load word positions progressively
- **Audio Preloading**: Preload next ayah audio for smooth playback

## Phase 4: Deployment and Scaling

### 4.1. Database Optimization

- **Indexing**: Create indexes on frequently queried columns
- **Partitioning**: Consider partitioning large tables by surah
- **Caching**: Implement Redis for frequently accessed data

### 4.2. Audio Delivery

- **CDN**: Use CDN for audio file delivery
- **Compression**: Optimize audio files for web delivery
- **Streaming**: Implement audio streaming for large files

### 4.3. API Performance

- **Pagination**: Implement pagination for large result sets
- **Rate Limiting**: Implement rate limiting to prevent abuse
- **Monitoring**: Add logging and monitoring for API performance

## Phase 5: Testing and Quality Assurance

### 5.1. Unit Testing

- Test all API endpoints
- Test database operations
- Test audio timing calculations

### 5.2. Integration Testing

- Test frontend-backend integration
- Test audio synchronization
- Test cross-browser compatibility

### 5.3. Performance Testing

- Load testing for concurrent users
- Audio streaming performance
- Database query optimization

## Conclusion

This implementation plan provides a comprehensive roadmap for building a Quranic Mushaf view with FastAPI backend. The approach leverages the best practices and data sources identified through our research of QUL, Quran.com, open-mushaf, and quran-align projects.

The modular architecture ensures scalability and maintainability, while the word-level database organization enables precise audio synchronization and interactive features that enhance the user's Quranic reading experience.

