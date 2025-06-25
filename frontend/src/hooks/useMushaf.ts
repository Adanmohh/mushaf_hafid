import { useState, useEffect } from 'react';
import { mushafApi } from '../services/api';
import { QulPageResponse, MushafLayout, QulWord } from '../types';

export const useMushaf = (layoutId: number = 1, initialPage: number = 1) => {
  const [layouts, setLayouts] = useState<MushafLayout[]>([]);
  const [currentPage, setCurrentPage] = useState<QulPageResponse | null>(null);
  const [currentPageNumber, setCurrentPageNumber] = useState(initialPage);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedWord, setSelectedWord] = useState<QulWord | null>(null);

  // Load layouts
  useEffect(() => {
    const loadLayouts = async () => {
      try {
        const response = await mushafApi.getLayouts();
        setLayouts(response.layouts);
      } catch (err) {
        console.error('Failed to load layouts:', err);
        setError('Failed to load Mushaf layouts');
      }
    };
    loadLayouts();
  }, []);

  // Load page data
  useEffect(() => {
    const loadPage = async () => {
      if (!layoutId) return;
      
      setLoading(true);
      setError(null);
      
      try {
        const response = await mushafApi.getPage(layoutId, currentPageNumber);
        setCurrentPage(response);
      } catch (err) {
        console.error('Failed to load page:', err);
        setError(`Failed to load page ${currentPageNumber}`);
      } finally {
        setLoading(false);
      }
    };

    loadPage();
  }, [layoutId, currentPageNumber]);

  const goToPage = (pageNumber: number) => {
    if (pageNumber < 1) return;
    const maxPages = layouts.find(l => l.id === layoutId)?.total_pages || 604;
    if (pageNumber > maxPages) return;
    
    setCurrentPageNumber(pageNumber);
  };

  const nextPage = () => goToPage(currentPageNumber + 1);
  const previousPage = () => goToPage(currentPageNumber - 1);

  const goToAyah = async (surah: number, ayah: number) => {
    try {
      setLoading(true);
      const location = await mushafApi.findAyahLocation(surah, ayah, layoutId);
      goToPage(location.page_number);
    } catch (err) {
      console.error('Failed to find ayah location:', err);
      setError(`Failed to find ayah ${surah}:${ayah}`);
    } finally {
      setLoading(false);
    }
  };

  return {
    layouts,
    currentPage,
    currentPageNumber,
    loading,
    error,
    selectedWord,
    setSelectedWord,
    goToPage,
    nextPage,
    previousPage,
    goToAyah
  };
};