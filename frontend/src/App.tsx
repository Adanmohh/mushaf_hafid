import React, { useState } from 'react';
import { useMushaf } from './hooks/useMushaf';
import { useAudio } from './hooks/useAudio';
import MushafPage from './components/MushafPage';
import AudioPlayer from './components/AudioPlayer';
import SearchBox from './components/SearchBox';
import WordInfo from './components/WordInfo';
import Navigation from './components/Navigation';
import { QulWord, SearchResult } from './types';

const App: React.FC = () => {
  const {
    layouts,
    currentPage,
    currentPageNumber,
    loading,
    error,
    selectedWord,
    setSelectedWord,
    goToPage,
    nextPage,
    previousPage,
    goToAyah
  } = useMushaf(1, 1);

  const {
    isPlaying,
    currentTime,
    duration,
    highlightedWordId,
    audioRef,
    loadAyahAudio,
    togglePlayPause,
    seekTo,
    playWord
  } = useAudio();

  const [searchResults, setSearchResults] = useState<SearchResult[]>([]);

  const handleWordClick = (word: QulWord) => {
    setSelectedWord(word);
  };

  const handleWordDoubleClick = async (word: QulWord) => {
    setSelectedWord(word);
    // Note: QulWord doesn't have surah/ayah directly, would need to get from API
    // For now, just set selected word
  };

  const handlePlayWord = (wordId: number) => {
    playWord(wordId, 1);
  };

  const handleSearchResult = (results: SearchResult[]) => {
    setSearchResults(results);
  };

  const handleAyahNavigation = (surah: number, ayah: number) => {
    goToAyah(surah, ayah);
  };

  const currentLayout = layouts.find(l => l.id === 1);
  const totalPages = currentLayout?.total_pages || 604;

  return (
    <div className="mushaf-container">
      <header className="mushaf-header">
        <h1 className="mushaf-title">
          مصحف حافظ - Mushaf Hafid
        </h1>
        <p className="mushaf-subtitle">
          نسخة تفاعلية من المصحف الشريف
        </p>
      </header>

      <div className="controls">
        <div className="controls-content">
          <SearchBox 
            onSearchResult={handleSearchResult}
            onAyahNavigation={handleAyahNavigation}
          />
          
          <div style={{ marginLeft: 'auto', display: 'flex', gap: '10px' }}>
            <button className="btn btn-secondary" onClick={previousPage}>
              ← Previous
            </button>
            <button className="btn btn-secondary" onClick={nextPage}>
              Next →
            </button>
          </div>
        </div>
      </div>

      <Navigation 
        currentPage={currentPageNumber}
        totalPages={totalPages}
        onPageChange={goToPage}
        onAyahNavigation={handleAyahNavigation}
      />

      <AudioPlayer 
        isPlaying={isPlaying}
        currentTime={currentTime}
        duration={duration}
        onTogglePlayPause={togglePlayPause}
        onSeek={seekTo}
        audioRef={audioRef}
      />

      {loading && (
        <div className="loading">
          Loading page {currentPageNumber}...
        </div>
      )}

      {error && (
        <div className="error">
          {error}
        </div>
      )}

      {currentPage && !loading && (
        <MushafPage 
          page={currentPage}
          selectedWord={selectedWord}
          highlightedWordId={highlightedWordId}
          onWordClick={handleWordClick}
          onWordDoubleClick={handleWordDoubleClick}
        />
      )}

      <WordInfo 
        word={selectedWord}
        onPlayWord={handlePlayWord}
      />

      {searchResults.length > 0 && (
        <div className="search-results-summary" style={{
          background: 'white',
          padding: '15px',
          borderRadius: '8px',
          marginTop: '20px',
          boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)'
        }}>
          <h3>Search Results ({searchResults.length} found)</h3>
          <div style={{ maxHeight: '200px', overflowY: 'auto' }}>
            {searchResults.slice(0, 5).map((result, index) => (
              <div key={index} style={{ 
                padding: '8px 0', 
                borderBottom: '1px solid #f1f1f1',
                cursor: 'pointer'
              }}
              onClick={() => handleAyahNavigation(result.surah, result.ayah)}>
                <div className="arabic-text">{result.text}</div>
                <div style={{ fontSize: '14px', color: '#666' }}>
                  {result.translation} - Surah {result.surah}:{result.ayah}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      <footer style={{ 
        textAlign: 'center', 
        padding: '20px',
        borderTop: '1px solid #e9ecef',
        background: '#f8f9fa',
        color: '#6c757d',
        fontSize: '0.9rem'
      }}>
        <p>
          التخطيط: {currentLayout?.name || 'جاري التحميل...'} | 
          الصفحة: {currentPageNumber} من {totalPages}
        </p>
        <p style={{ fontSize: '0.8rem', marginTop: '5px', direction: 'ltr' }}>
          Mushaf Hafid - Interactive Quranic Mushaf
        </p>
      </footer>
    </div>
  );
};

export default App;