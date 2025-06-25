import axios from 'axios';
import { LayoutsResponse, PageResponse, SearchResponse, AyahAudio, QulPageResponse, QulSurahNamesResponse, QulSurahInfo } from '../types';

const API_BASE_URL = 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
});

export const mushafApi = {
  // Get all available layouts
  getLayouts: async (): Promise<LayoutsResponse> => {
    const response = await api.get('/qul/layouts');
    return response.data;
  },

  // Get specific page data (QUL format)
  getPage: async (layoutId: number, pageNumber: number): Promise<QulPageResponse> => {
    const response = await api.get(`/qul/page/${pageNumber}`);
    return response.data;
  },

  // Find ayah location
  findAyahLocation: async (surah: number, ayah: number, layoutId = 1) => {
    const response = await api.get(`/mushaf/surah/${surah}/ayah/${ayah}/page`, {
      params: { layout_id: layoutId }
    });
    return response.data;
  },

  // Search Quran (QUL format)
  search: async (query: string, limit = 20): Promise<SearchResponse> => {
    const response = await api.get('/qul/search', {
      params: { q: query, limit }
    });
    return response.data;
  },

  // Get search suggestions
  getSearchSuggestions: async (query: string, limit = 10) => {
    const response = await api.get('/search/suggestions', {
      params: { q: query, limit }
    });
    return response.data;
  },

  // Get recitations
  getRecitations: async () => {
    const response = await api.get('/audio/recitations');
    return response.data;
  },

  // Get word audio timing
  getWordAudio: async (wordId: number, recitationId: number) => {
    const response = await api.get(`/audio/word/${wordId}/recitation/${recitationId}`);
    return response.data;
  },

  // Get ayah audio timing
  getAyahAudio: async (surah: number, ayah: number, recitationId: number): Promise<AyahAudio> => {
    const response = await api.get(`/audio/ayah/${surah}/${ayah}/recitation/${recitationId}`);
    return response.data;
  },

  // QUL-specific methods
  getSurahNames: async (): Promise<QulSurahNamesResponse> => {
    const response = await api.get('/qul/surah-names');
    return response.data;
  },

  getSurahInfo: async (surahNumber: number): Promise<QulSurahInfo> => {
    const response = await api.get(`/qul/surah/${surahNumber}`);
    return response.data;
  },

  getAyahWords: async (surahNumber: number, ayahNumber: number) => {
    const response = await api.get(`/qul/ayah/${surahNumber}/${ayahNumber}`);
    return response.data;
  },

  getWordsRange: async (firstWordId: number, lastWordId: number) => {
    const response = await api.get(`/qul/words/${firstWordId}/${lastWordId}`);
    return response.data;
  }
};

export default api;