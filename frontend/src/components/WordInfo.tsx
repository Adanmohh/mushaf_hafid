import React from 'react';
import { QulWord } from '../types';

interface WordInfoProps {
  word: QulWord | null;
  onPlayWord: (wordId: number) => void;
}

const WordInfo: React.FC<WordInfoProps> = ({ word, onPlayWord }) => {
  if (!word) return null;

  return (
    <div className="word-info">
      <h3>Word Information</h3>
      
      <div className="word-info-content">
        <div className="arabic-word">
          {word.text}
        </div>
        
        <p><strong>Word ID:</strong> {word.word_id}</p>
        <p><strong>Text:</strong> {word.text}</p>
        
        <div style={{ marginTop: '15px', textAlign: 'center' }}>
          <button 
            className="btn"
            onClick={() => onPlayWord(word.word_id)}
          >
            🔊 Play Word
          </button>
        </div>
      </div>
    </div>
  );
};

export default WordInfo;