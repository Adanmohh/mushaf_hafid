"""
SQLAlchemy database models for Quranic Mushaf data
"""

from sqlalchemy import Column, Integer, String, ForeignKey, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class MushafLayout(Base):
    __tablename__ = "mushaf_layouts"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    total_pages = Column(Integer, nullable=False)
    lines_per_page = Column(Integer, nullable=False)
    font_name = Column(String, nullable=False)
    
    # Relationships
    pages = relationship("Page", back_populates="layout")
    word_positions = relationship("WordPosition", back_populates="layout")

class Page(Base):
    __tablename__ = "pages"
    
    id = Column(Integer, primary_key=True, index=True)
    mushaf_layout_id = Column(Integer, ForeignKey("mushaf_layouts.id"), nullable=False)
    page_number = Column(Integer, nullable=False)
    image_url = Column(String)
    
    # Relationships
    layout = relationship("MushafLayout", back_populates="pages")
    lines = relationship("Line", back_populates="page")

class Line(Base):
    __tablename__ = "lines"
    
    id = Column(Integer, primary_key=True, index=True)
    page_id = Column(Integer, ForeignKey("pages.id"), nullable=False)
    line_number = Column(Integer, nullable=False)
    
    # Relationships
    page = relationship("Page", back_populates="lines")
    words = relationship("Word", back_populates="line")

class Word(Base):
    __tablename__ = "words"
    
    id = Column(Integer, primary_key=True, index=True)
    line_id = Column(Integer, ForeignKey("lines.id"), nullable=False)
    word_position = Column(Integer, nullable=False)
    surah_number = Column(Integer, nullable=False)
    ayah_number = Column(Integer, nullable=False)
    word_text_uthmani = Column(Text, nullable=False)
    translation_en = Column(Text)
    transliteration_en = Column(Text)
    
    # Relationships
    line = relationship("Line", back_populates="words")
    positions = relationship("WordPosition", back_populates="word")
    audio_timings = relationship("AudioTiming", back_populates="word")

class WordPosition(Base):
    __tablename__ = "word_positions"
    
    id = Column(Integer, primary_key=True, index=True)
    word_id = Column(Integer, ForeignKey("words.id"), nullable=False)
    mushaf_layout_id = Column(Integer, ForeignKey("mushaf_layouts.id"), nullable=False)
    page_number = Column(Integer, nullable=False)
    line_number = Column(Integer, nullable=False)
    x_coordinate = Column(Integer, nullable=False)
    y_coordinate = Column(Integer, nullable=False)
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    
    # Relationships
    word = relationship("Word", back_populates="positions")
    layout = relationship("MushafLayout", back_populates="word_positions")

class Recitation(Base):
    __tablename__ = "recitations"
    
    id = Column(Integer, primary_key=True, index=True)
    reciter_name = Column(String, nullable=False)
    style = Column(String, nullable=False)
    
    # Relationships
    audio_timings = relationship("AudioTiming", back_populates="recitation")

class AudioTiming(Base):
    __tablename__ = "audio_timings"
    
    id = Column(Integer, primary_key=True, index=True)
    word_id = Column(Integer, ForeignKey("words.id"), nullable=False)
    recitation_id = Column(Integer, ForeignKey("recitations.id"), nullable=False)
    start_time = Column(Integer, nullable=False)  # in milliseconds
    end_time = Column(Integer, nullable=False)    # in milliseconds
    audio_file_url = Column(String, nullable=False)
    
    # Relationships
    word = relationship("Word", back_populates="audio_timings")
    recitation = relationship("Recitation", back_populates="audio_timings")

