import React, { useState, useEffect } from 'react';
import { mushafApi } from './services/api';
import { QulPageResponse, QulWord, SurahInfo } from './types';
import MushafPage from './components/MushafPage';
import Navigation from './components/Navigation';
import SearchBox from './components/SearchBox';
import WordInfo from './components/WordInfo';
import './index.css';

function App() {
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(604); // Standard Mushaf page count
  const [pageData, setPageData] = useState<QulPageResponse | null>(null);
  const [selectedWord, setSelectedWord] = useState<QulWord | null>(null);
  const [highlightedWordId, setHighlightedWordId] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [surahs, setSurahs] = useState<SurahInfo[]>([]);

  // Load initial data
  useEffect(() => {
    loadInitialData();
  }, []);

  // Load page when currentPage changes
  useEffect(() => {
    loadPage(currentPage);
  }, [currentPage]);

  const loadInitialData = async () => {
    try {
      // Load available layouts and surahs
      const [layoutsResponse, surahsResponse] = await Promise.all([
        mushafApi.getLayouts(),
        mushafApi.getSurahNames()
      ]);

      setSurahs(surahsResponse.surahs);

      // Update total pages if available from layouts
      if (layoutsResponse.layouts.length > 0) {
        setTotalPages(layoutsResponse.layouts[0].total_pages);
      }
    } catch (err) {
      console.error('Error loading initial data:', err);
      setError('Failed to load initial data');
    }
  };

  const loadPage = async (pageNumber: number) => {
    setLoading(true);
    setError(null);
    
    try {
      const data = await mushafApi.getPage(pageNumber);
      setPageData(data);
    } catch (err) {
      console.error('Error loading page:', err);
      setError(`Failed to load page ${pageNumber}`);
    } finally {
      setLoading(false);
    }
  };

  const handlePageChange = (page: number) => {
    if (page >= 1 && page <= totalPages) {
      setCurrentPage(page);
      setSelectedWord(null);
      setHighlightedWordId(null);
    }
  };

  const handleAyahNavigation = async (surah: number, ayah: number) => {
    try {
      setLoading(true);
      const result = await mushafApi.findAyahPage(surah, ayah);
      setCurrentPage(result.page_number);
    } catch (err) {
      console.error('Error navigating to ayah:', err);
      setError(`Failed to navigate to Surah ${surah}, Ayah ${ayah}`);
    } finally {
      setLoading(false);
    }
  };

  const handleWordClick = (word: QulWord) => {
    setSelectedWord(word);
    setHighlightedWordId(word.word_id);
  };

  const handleWordDoubleClick = async (word: QulWord) => {
    // Future: Load and play ayah audio
    console.log('Double clicked word:', word);
  };

  const handlePlayWord = async (wordId: number) => {
    try {
      const audioData = await mushafApi.getWordAudio(wordId, 1);
      console.log('Playing word audio:', audioData);
      // Future: Implement actual audio playback
    } catch (err) {
      console.error('Error playing word audio:', err);
    }
  };

  const handleSearchResult = (results: any[]) => {
    // Future: Handle search result highlighting
    console.log('Search results:', results);
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1 className="app-title">Mushaf Hafid - Interactive Quranic Mushaf</h1>
        <p className="app-subtitle">
          Word-level Interactive Quran with QUL Rendering • Page {currentPage} of {totalPages}
        </p>
      </header>

      <div className="app-toolbar">
        <Navigation
          currentPage={currentPage}
          totalPages={totalPages}
          onPageChange={handlePageChange}
          onAyahNavigation={handleAyahNavigation}
        />
        
        <SearchBox
          onSearchResult={handleSearchResult}
          onAyahNavigation={handleAyahNavigation}
        />
      </div>

      {error && (
        <div className="error-message">
          <p>⚠️ {error}</p>
        </div>
      )}

      <div className="app-content">
        <main className="main-content">
          {loading ? (
            <div className="loading">
              <p>Loading page {currentPage}...</p>
            </div>
          ) : pageData ? (
            <MushafPage
              page={pageData}
              selectedWord={selectedWord}
              highlightedWordId={highlightedWordId}
              onWordClick={handleWordClick}
              onWordDoubleClick={handleWordDoubleClick}
            />
          ) : (
            <div className="no-data">
              <p>No page data available</p>
            </div>
          )}
        </main>

        <aside className="sidebar">
          <WordInfo
            word={selectedWord}
            onPlayWord={handlePlayWord}
          />
          
          {surahs.length > 0 && (
            <div className="surah-list">
              <h3>Available Surahs</h3>
              <div className="surah-list-content">
                {surahs.slice(0, 10).map((surah) => (
                  <button
                    key={surah.surah_number}
                    className="surah-button"
                    onClick={() => handleAyahNavigation(surah.surah_number, 1)}
                  >
                    {surah.surah_number}. {surah.name_english}
                  </button>
                ))}
              </div>
            </div>
          )}
        </aside>
      </div>

      <footer className="app-footer">
        <p>
          Built with QUL Rendering Logic • 
          Showing {pageData?.total_lines || 0} lines • 
          {pageData ? pageData.lines.reduce((total, line) => total + line.words.length, 0) : 0} words
        </p>
      </footer>
    </div>
  );
}

export default App;