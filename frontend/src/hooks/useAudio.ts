import { useState, useRef, useEffect } from 'react';
import { mushafApi } from '../services/api';
import { AyahAudio } from '../types';

export const useAudio = () => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [highlightedWordId, setHighlightedWordId] = useState<number | null>(null);
  const [currentAyahAudio, setCurrentAyahAudio] = useState<AyahAudio | null>(null);
  const audioRef = useRef<HTMLAudioElement | null>(null);

  useEffect(() => {
    const audio = audioRef.current;
    if (!audio) return;

    const updateTime = () => setCurrentTime(audio.currentTime * 1000);
    const updateDuration = () => setDuration(audio.duration * 1000);
    
    audio.addEventListener('timeupdate', updateTime);
    audio.addEventListener('loadedmetadata', updateDuration);
    audio.addEventListener('ended', () => setIsPlaying(false));

    return () => {
      audio.removeEventListener('timeupdate', updateTime);
      audio.removeEventListener('loadedmetadata', updateDuration);
      audio.removeEventListener('ended', () => setIsPlaying(false));
    };
  }, [currentAyahAudio]);

  // Update highlighted word based on current time
  useEffect(() => {
    if (!currentAyahAudio || !isPlaying) {
      setHighlightedWordId(null);
      return;
    }

    const currentWord = currentAyahAudio.word_timings.find(
      timing => currentTime >= timing.start_time && currentTime <= timing.end_time
    );

    setHighlightedWordId(currentWord?.word_id || null);
  }, [currentTime, currentAyahAudio, isPlaying]);

  const loadAyahAudio = async (surah: number, ayah: number, recitationId: number = 1) => {
    try {
      const ayahAudio = await mushafApi.getAyahAudio(surah, ayah, recitationId);
      setCurrentAyahAudio(ayahAudio);
      
      if (audioRef.current) {
        audioRef.current.src = ayahAudio.audio_url;
        audioRef.current.load();
      }
    } catch (error) {
      console.error('Failed to load ayah audio:', error);
    }
  };

  const play = () => {
    if (audioRef.current) {
      audioRef.current.play();
      setIsPlaying(true);
    }
  };

  const pause = () => {
    if (audioRef.current) {
      audioRef.current.pause();
      setIsPlaying(false);
    }
  };

  const togglePlayPause = () => {
    if (isPlaying) {
      pause();
    } else {
      play();
    }
  };

  const seekTo = (timeMs: number) => {
    if (audioRef.current) {
      audioRef.current.currentTime = timeMs / 1000;
      setCurrentTime(timeMs);
    }
  };

  const playWord = async (wordId: number, recitationId: number = 1) => {
    try {
      const wordAudio = await mushafApi.getWordAudio(wordId, recitationId);
      
      if (audioRef.current) {
        audioRef.current.src = wordAudio.audio_url;
        audioRef.current.currentTime = wordAudio.start_time / 1000;
        audioRef.current.play();
        setIsPlaying(true);
        
        // Stop at end time
        setTimeout(() => {
          if (audioRef.current) {
            audioRef.current.pause();
            setIsPlaying(false);
          }
        }, wordAudio.duration);
      }
    } catch (error) {
      console.error('Failed to play word audio:', error);
    }
  };

  return {
    isPlaying,
    currentTime,
    duration,
    highlightedWordId,
    currentAyahAudio,
    audioRef,
    loadAyahAudio,
    play,
    pause,
    togglePlayPause,
    seekTo,
    playWord
  };
};