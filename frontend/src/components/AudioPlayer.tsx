import React from 'react';

interface AudioPlayerProps {
  isPlaying: boolean;
  currentTime: number;
  duration: number;
  onTogglePlayPause: () => void;
  onSeek: (time: number) => void;
  audioRef: React.RefObject<HTMLAudioElement>;
}

const AudioPlayer: React.FC<AudioPlayerProps> = ({
  isPlaying,
  currentTime,
  duration,
  onTogglePlayPause,
  onSeek,
  audioRef
}) => {
  const formatTime = (timeMs: number) => {
    const seconds = Math.floor(timeMs / 1000);
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
  };

  const handleProgressClick = (e: React.MouseEvent<HTMLDivElement>) => {
    const rect = e.currentTarget.getBoundingClientRect();
    const percent = (e.clientX - rect.left) / rect.width;
    const newTime = percent * duration;
    onSeek(newTime);
  };

  const progressPercent = duration > 0 ? (currentTime / duration) * 100 : 0;

  return (
    <div className="audio-controls">
      <button 
        className="btn"
        onClick={onTogglePlayPause}
        disabled={duration === 0}
      >
        {isPlaying ? '⏸️ Pause' : '▶️ Play'}
      </button>
      
      <div className="time-display">
        {formatTime(currentTime)} / {formatTime(duration)}
      </div>
      
      <div 
        className="progress-bar" 
        onClick={handleProgressClick}
        style={{ cursor: duration > 0 ? 'pointer' : 'default' }}
      >
        <div 
          className="progress-fill" 
          style={{ width: `${progressPercent}%` }}
        />
      </div>
      
      <audio ref={audioRef} preload="metadata" />
    </div>
  );
};

export default AudioPlayer;