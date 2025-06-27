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

  async getAyah(surahNumber: number, ayahNumber: number): Promise<{
    surah_number: number;
    ayah_number: number;
    text: string;
    words: Array<{ word_id: number; text: string }>;
    page_number: number | null;
    surah_name: string | null;
    surah_arabic: string | null;
  }> {
    const response = await api.get(`/qul/ayah/${surahNumber}/${ayahNumber}`);
    return response.data;
  },

  async search(query: string, limit: number = 20): Promise<{
    results: SearchResult[];
    total_found: number;
    query: string;
  }> {
    const response = await api.get('/qul/search', {
      params: { query, limit }
    });
    return response.data;
  },

  async getStats(): Promise<{
    total_words: number;
    total_pages: number;
    total_surahs: number;
    total_ayahs: number;
    layout_name: string;
    font_system: string;
  }> {
    const response = await api.get('/qul/stats');
    return response.data;
  },

  // Audio endpoints (legacy support)
  async getRecitations(): Promise<{ recitations: Recitation[] }> {
    try {
      const response = await api.get('/audio/recitations');
      return response.data;
    } catch (error) {
      console.warn('Audio recitations not available:', error);
      return { recitations: [] };
    }
  },

  async getWordAudio(wordId: number, recitationId: string = 'default'): Promise<{
    word_id: number;
    audio_url: string;
    recitation_id: string;
  }> {
    try {
      const response = await api.get(`/audio/word/${wordId}`, {
        params: { recitation_id: recitationId }
      });
      return response.data;
    } catch (error) {
      console.warn(`Audio for word ${wordId} not available:`, error);
      throw error;
    }
  },

  async getPageAudio(pageNumber: number, recitationId: string = 'default'): Promise<{
    page_number: number;
    audio_segments: Array<{
      word_id: number;
      start_time: number;
      end_time: number;
      audio_url: string;
    }>;
    recitation_id: string;
  }> {
    try {
      const response = await api.get(`/audio/page/${pageNumber}`, {
        params: { recitation_id: recitationId }
      });
      return response.data;
    } catch (error) {
      console.warn(`Audio for page ${pageNumber} not available:`, error);
      throw error;
    }
  },

  // Font endpoint
  async getPageFont(pageNumber: number): Promise<Blob> {
    const response = await api.get(`/fonts/${pageNumber}`, {
      responseType: 'blob'
    });
    return response.data;
  },

  // Health check
  async healthCheck(): Promise<{
    status: string;
    qul_database: string;
    fonts: string;
    total_pages: number;
    font_system: string;
  }> {
    const response = await api.get('/health');
    return response.data;
  }
};

export default mushafApi;