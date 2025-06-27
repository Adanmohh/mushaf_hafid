import React from 'react';
import { QulPageResponse, QulWord } from '../types';

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
  const getWordClassName = (word: QulWord) => {
    let className = 'mushaf-word arabic-text';
    
    if (selectedWord?.word_id === word.word_id) {
      className += ' selected';
    }
    
    if (highlightedWordId === word.word_id) {
      className += ' highlighted';
    }
    
    return className;
  };

  const getLineClassName = (lineType: string, isCentered: boolean) => {
    let className = 'mushaf-line';
    if (lineType === 'surah_name') {
      className += ' surah-name';
    } else if (lineType === 'basmallah') {
      className += ' basmallah';
    }
    if (isCentered) {
      className += ' centered';
    }
    return className;
  };

  return (
    <div className="mushaf-page">
      <div className="page-header">
        <h2 className="page-number">Page {page.page_number}</h2>
      </div>
      
      <div className="page-content">
        {page.lines.map((line) => (
          <div
            key={line.line_number}
            className={getLineClassName(line.line_type, line.is_centered)}
            data-line-type={line.line_type}
          >
            {line.line_type === 'ayah' && line.words.length > 0 ? (
              // Render individual words for ayah lines
              line.words.map((word) => (
                <span
                  key={word.word_id}
                  className={getWordClassName(word)}
                  onClick={() => onWordClick(word)}
                  onDoubleClick={() => onWordDoubleClick(word)}
                  title={`Word ID: ${word.word_id}`}
                >
                  {word.text}
                </span>
              ))
            ) : (
              // Render complete content for surah names and basmallah
              <span className="line-content">
                {line.content}
              </span>
            )}
          </div>
        ))}
      </div>
      
      <div className="page-stats">
        <p>
          Page: {page.page_number} | Lines: {page.total_lines} | 
          Words: {page.lines.reduce((total, line) => total + line.words.length, 0)}
        </p>
      </div>
    </div>
  );
};

export default MushafPage;