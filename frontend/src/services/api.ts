import axios from 'axios';
import { 
  QulPageResponse, 
  QulLayoutInfo, 
  SurahInfo, 
  SearchResult,
  WordDetails,
  Recitation
} from '../types';

const API_BASE_URL = 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

export const mushafApi = {
  // QUL Layout endpoints
  async getLayouts(): Promise<{ layouts: QulLayoutInfo[] }> {
    const response = await api.get('/qul/layouts');
    return response.data;
  },

  async getPage(pageNumber: number): Promise<QulPageResponse> {
    const response = await api.get(`/qul/page/${pageNumber}`);
    return response.data;
  },

  async getSurahNames(): Promise<{ surah_names: Record<number, string>; surahs: SurahInfo[] }> {
    const response = await api.get('/qul/surah-names');
    return response.data;
  },

  async getSurahInfo(surahNumber: number): Promise<SurahInfo> {
    const response = await api.get(`/qul/surah/${surahNumber}`);
    return response.data;
  },

  async getAyahWords(surahNumber: number, ayahNumber: number): Promise<{
    surah: number;
    ayah: number;
    words: WordDetails[];
    text: string;
  }> {
    const response = await api.get(`/qul/ayah/${surahNumber}/${ayahNumber}`);
    return response.data;
  },

  async getWordsRange(firstWordId: number, lastWordId: number): Promise<{
    first_word_id: number;
    last_word_id: number;
    words: WordDetails[];
    combined_text: string;
  }> {
    const response = await api.get(`/qul/words/${firstWordId}/${lastWordId}`);
    return response.data;
  },

  // Search endpoints
  async search(query: string, limit: number = 20): Promise<{
    query: string;
    results_count: number;
    results: SearchResult[];
  }> {
    const response = await api.get('/qul/search', {
      params: { q: query, limit }
    });
    return response.data;
  },

  // Navigation helpers
  async findAyahPage(surahNumber: number, ayahNumber: number): Promise<{ page_number: number }> {
    // This would need to be implemented in the backend
    // For now, return page 1 for Al-Fatiha, page 2 for Al-Baqarah
    if (surahNumber === 1) {
      return { page_number: 1 };
    } else if (surahNumber === 2) {
      return { page_number: 2 };
    }
    return { page_number: 1 };
  },

  // Audio endpoints (for future implementation)
  async getRecitations(): Promise<{ recitations: Recitation[] }> {
    // Placeholder for audio functionality
    return {
      recitations: [
        { id: 1, reciter_name: "Abdul Basit Abdul Samad", style: "Mujawwad" }
      ]
    };
  },

  async getWordAudio(wordId: number, recitationId: number): Promise<{
    word_id: number;
    audio_url: string;
    start_time: number;
    end_time: number;
  }> {
    // Placeholder for audio functionality
    return {
      word_id: wordId,
      audio_url: `/static/audio/word_${wordId}.mp3`,
      start_time: 0,
      end_time: 1000
    };
  }
};

export default api;