import React, { useState } from 'react';
import { mushafApi } from '../services/api';
import { SearchResult } from '../types';

interface SearchBoxProps {
  onSearchResult: (results: SearchResult[]) => void;
  onAyahNavigation: (surah: number, ayah: number) => void;
}

const SearchBox: React.FC<SearchBoxProps> = ({ onSearchResult, onAyahNavigation }) => {
  const [query, setQuery] = useState('');
  const [isSearching, setIsSearching] = useState(false);
  const [searchResults, setSearchResults] = useState<SearchResult[]>([]);
  const [showResults, setShowResults] = useState(false);

  const handleSearch = async () => {
    if (!query.trim()) return;

    setIsSearching(true);
    try {
      const response = await mushafApi.search(query, 10);
      setSearchResults(response.results);
      setShowResults(true);
      onSearchResult(response.results);
    } catch (error) {
      console.error('Search failed:', error);
    } finally {
      setIsSearching(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  const handleResultClick = (result: SearchResult) => {
    onAyahNavigation(result.surah, result.ayah);
    setShowResults(false);
  };

  return (
    <div className="search-container">
      <input
        type="text"
        className="search-input"
        placeholder="ابحث في النص القرآني أو الترجمة أو النطق..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyPress={handleKeyPress}
      />
      <button 
        className="btn" 
        onClick={handleSearch}
        disabled={isSearching || !query.trim()}
      >
        {isSearching ? 'جاري البحث...' : 'بحث'}
      </button>
      
      {showResults && searchResults.length > 0 && (
        <div className="search-results" style={{
          position: 'absolute',
          top: '100%',
          left: 0,
          right: 0,
          background: 'white',
          border: '1px solid #e2e8f0',
          borderRadius: '6px',
          maxHeight: '300px',
          overflowY: 'auto',
          zIndex: 1000,
          boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)'
        }}>
          {searchResults.map((result, index) => (
            <div
              key={index}
              className="search-result-item"
              style={{
                padding: '10px',
                borderBottom: '1px solid #f1f1f1',
                cursor: 'pointer',
                '&:hover': { backgroundColor: '#f8f9fa' }
              }}
              onClick={() => handleResultClick(result)}
              onMouseEnter={(e) => {
                (e.target as HTMLElement).style.backgroundColor = '#f8f9fa';
              }}
              onMouseLeave={(e) => {
                (e.target as HTMLElement).style.backgroundColor = 'white';
              }}
            >
              <div className="arabic-text" style={{ fontSize: '16px', marginBottom: '5px' }}>
                {result.text}
              </div>
              <div style={{ fontSize: '14px', color: '#666' }}>
                {result.translation}
              </div>
              <div style={{ fontSize: '12px', color: '#999' }}>
                Surah {result.surah}, Ayah {result.ayah}
                {result.page && ` • Page ${result.page}`}
              </div>
            </div>
          ))}
        </div>
      )}
      
      {showResults && (
        <button
          className="btn btn-secondary"
          onClick={() => setShowResults(false)}
          style={{ marginLeft: '10px' }}
        >
          إغلاق
        </button>
      )}
    </div>
  );
};

export default SearchBox;