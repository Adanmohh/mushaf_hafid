export interface WordPosition {
  x: number;
  y: number;
  width: number;
  height: number;
}

export interface Word {
  id: number;
  text: string;
  surah: number;
  ayah: number;
  position: WordPosition;
  translation?: string;
  transliteration?: string;
}

export interface Line {
  line_number: number;
  words: Word[];
}

export interface Page {
  page_number: number;
  layout_id: number;
  image_url?: string;
  lines: Line[];
}

export interface MushafLayout {
  id: number;
  name: string;
  total_pages: number;
  lines_per_page: number;
  font_name: string;
}

export interface PageResponse {
  page: Page;
}

export interface LayoutsResponse {
  layouts: MushafLayout[];
}

export interface AudioTiming {
  word_id: number;
  start_time: number;
  end_time: number;
}

export interface AyahAudio {
  surah: number;
  ayah: number;
  recitation_id: number;
  audio_url: string;
  word_timings: AudioTiming[];
}

export interface SearchResult {
  word_id: number;
  surah: number;
  ayah: number;
  text: string;
  translation?: string;
  transliteration?: string;
  page?: number;
  line?: number;
}

export interface SearchResponse {
  query: string;
  results_count: number;
  results: SearchResult[];
}

// QUL-specific types
export interface QulWord {
  word_id: number;
  text: string;
}

export interface QulLine {
  line_number: number;
  line_type: 'surah_name' | 'ayah' | 'basmallah';
  is_centered: boolean;
  content: string;
  words: QulWord[];
  first_word_id?: number;
  last_word_id?: number;
  surah_number?: number;
}

export interface QulPageResponse {
  page_number: number;
  total_lines: number;
  lines: QulLine[];
}

export interface SurahInfo {
  surah_number: number;
  name_arabic: string;
  name_english: string;
  total_ayahs: number;
}

export interface QulSurahNamesResponse {
  surah_names: Record<number, string>;
  surahs: SurahInfo[];
}

// QUL-compatible types following newinfo.md structure
export interface QulLayoutInfo {
  id: number;
  name: string;
  total_pages: number;
  description: string;
}

// Audio types
export interface Recitation {
  id: number;
  reciter_name: string;
  style: string;
}

// Word details for info panel
export interface WordDetails extends QulWord {
  word_key: string;
  surah: number;
  ayah: number;
  translation?: string;
  transliteration?: string;
}