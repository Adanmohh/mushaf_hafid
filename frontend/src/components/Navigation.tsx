import React, { useState } from 'react';

interface NavigationProps {
  currentPage: number;
  totalPages: number;
  onPageChange: (page: number) => void;
  onAyahNavigation: (surah: number, ayah: number) => void;
}

const Navigation: React.FC<NavigationProps> = ({
  currentPage,
  totalPages,
  onPageChange,
  onAyahNavigation
}) => {
  const [pageInput, setPageInput] = useState(currentPage.toString());
  const [surahInput, setSurahInput] = useState('1');
  const [ayahInput, setAyahInput] = useState('1');

  const handlePageSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const page = parseInt(pageInput);
    if (page >= 1 && page <= totalPages) {
      onPageChange(page);
    }
  };

  const handleAyahSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const surah = parseInt(surahInput);
    const ayah = parseInt(ayahInput);
    if (surah >= 1 && surah <= 114 && ayah >= 1) {
      onAyahNavigation(surah, ayah);
    }
  };

  const canGoPrevious = currentPage > 1;
  const canGoNext = currentPage < totalPages;

  return (
    <div className="page-navigation">
      <button 
        className="btn"
        onClick={() => onPageChange(currentPage - 1)}
        disabled={!canGoPrevious}
      >
        ← السابقة
      </button>
      
      <form onSubmit={handlePageSubmit} className="navigation-form">
        <span>صفحة</span>
        <input
          type="number"
          min="1"
          max={totalPages}
          value={pageInput}
          onChange={(e) => setPageInput(e.target.value)}
          className="input"
          style={{ width: '60px' }}
        />
        <span>من {totalPages}</span>
        <button type="submit" className="btn btn-secondary" style={{ padding: '8px 15px' }}>
          اذهب
        </button>
      </form>
      
      <button 
        className="btn"
        onClick={() => onPageChange(currentPage + 1)}
        disabled={!canGoNext}
      >
        التالية →
      </button>
      
      <div style={{ margin: '0 20px', borderLeft: '2px solid #d4af37', height: '30px' }} />
      
      <form onSubmit={handleAyahSubmit} className="navigation-form">
        <span>اذهب إلى سورة</span>
        <input
          type="number"
          min="1"
          max="114"
          value={surahInput}
          onChange={(e) => setSurahInput(e.target.value)}
          className="input"
          style={{ width: '50px' }}
        />
        <span>آية</span>
        <input
          type="number"
          min="1"
          value={ayahInput}
          onChange={(e) => setAyahInput(e.target.value)}
          className="input"
          style={{ width: '50px' }}
        />
        <button type="submit" className="btn btn-secondary" style={{ padding: '8px 15px' }}>
          اذهب إلى الآية
        </button>
      </form>
    </div>
  );
};

export default Navigation;