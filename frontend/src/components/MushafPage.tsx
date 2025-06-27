import React, { useEffect, useState } from 'react';
import { QulPageResponse, QulWord, QulLine } from '../types';

interface MushafPageProps {
  page: QulPageResponse;
  selectedWord: QulWord | null;
  highlightedWordId: number | null;
  onWordClick: (word: QulWord) => void;
  onWordDoubleClick: (word: QulWord) => void;
}

const MushafPage: React.FC<MushafPageProps> = ({
  page,
  selectedWord,
  highlightedWordId,
  onWordClick,
  onWordDoubleClick
}) => {
  const [fontLoaded, setFontLoaded] = useState(false);

  // Load page-specific font
  useEffect(() => {
    if (page?.font_file && page?.page_number) {
      const fontName = `QPC-Page-${page.page_number}`;
      const fontUrl = `/static/fonts/p${page.page_number}.woff`;
      
      // Create font face
      const fontFace = new FontFace(fontName, `url(${fontUrl})`);
      
      fontFace.load().then(() => {
        document.fonts.add(fontFace);
        setFontLoaded(true);
      }).catch((error) => {
        console.warn(`Failed to load font for page ${page.page_number}:`, error);
        setFontLoaded(true); // Continue with fallback font
      });
    }
  }, [page?.page_number, page?.font_file]);

  const getWordClassName = (word: QulWord) => {
    let className = 'mushaf-word qul-arabic-text';
    
    if (selectedWord?.word_id === word.word_id) {
      className += ' selected';
    }
    
    if (highlightedWordId === word.word_id) {
      className += ' highlighted';
    }
    
    return className;
  };

  const getLineClassName = (line: QulLine) => {
    let className = 'mushaf-line';
    
    // Add line type specific classes
    if (line.line_type === 'surah_name') {
      className += ' surah-name-line';
    } else if (line.line_type === 'basmallah') {
      className += ' basmallah-line';
    } else if (line.line_type === 'ayah') {
      className += ' ayah-line';
    }
    
    // Add centering class
    if (line.is_centered) {
      className += ' centered';
    } else {
      className += ' justified';
    }
    
    return className;
  };

  const renderLine = (line: QulLine) => {
    const lineClass = getLineClassName(line);
    
    return (
      <div key={line.line_number} className={lineClass}>
        {line.line_type === 'surah_name' || line.line_type === 'basmallah' ? (
          // Render surah name or basmallah as single text
          <span className="special-text qul-arabic-text">
            {line.content}
          </span>
        ) : (
          // Render ayah words individually for interactivity
          line.words.map((word, wordIndex) => (
            <span
              key={`${line.line_number}-${word.word_id || wordIndex}`}
              className={getWordClassName(word)}
              onClick={() => word.word_id && onWordClick(word)}
              onDoubleClick={() => word.word_id && onWordDoubleClick(word)}
              data-word-id={word.word_id}
              data-line-number={line.line_number}
            >
              {word.text}
            </span>
          ))
        )}
      </div>
    );
  };

  if (!page) {
    return (
      <div className="mushaf-page loading">
        <div className="loading-message">Loading page...</div>
      </div>
    );
  }

  const pageClass = `mushaf-page page-${page.page_number} ${fontLoaded ? 'font-loaded' : 'font-loading'}`;
  const fontFamily = fontLoaded ? `QPC-Page-${page.page_number}, 'QPC V2 Font', 'Amiri', serif` : "'Amiri', serif";

  return (
    <div className={pageClass} style={{ fontFamily }}>
      <div className="page-header">
        <div className="page-number">Page {page.page_number}</div>
        <div className="page-stats">
          Lines: {page.total_lines} | 
          Font: {fontLoaded ? 'Loaded' : 'Loading...'}
        </div>
      </div>
      
      <div className="page-content">
        {page.lines.map(renderLine)}
      </div>
      
      <div className="page-footer">
        <div className="page-number-bottom">{page.page_number}</div>
      </div>
    </div>
  );
};

export default MushafPage;