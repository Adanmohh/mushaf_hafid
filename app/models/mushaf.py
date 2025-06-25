"""
Pydantic models for API requests and responses
"""

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

class PageResponse(BaseModel):
    page: Page

class LayoutsResponse(BaseModel):
    layouts: List[MushafLayout]

class ErrorResponse(BaseModel):
    message: str
    detail: Optional[str] = None