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
  word_key: string;
  surah: number;
  ayah: number;
  text: string;
  surah_name?: string;
  surah_arabic?: string;
  page?: number;
  translation?: string;
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
  font_file: string;
  font_path: string;
}

export interface SurahInfo {
  id: number;
  name_simple: string;
  name_arabic: string;
  verses_count: number;
}

export interface QulSurahNamesResponse {
  surah_names: Record<number, string>;
  surahs: SurahInfo[];
}

// QUL-compatible types following newinfo.md structure
export interface QulLayoutInfo {
  name: string;
  number_of_pages: number;
  lines_per_page: number;
  font_name: string;
}

// Audio types
export interface Recitation {
  id: string;
  name: string;
  style: string;
  url_template: string;
}

// Word details for info panel
export interface WordDetails {
  word_id: number;
  text: string;
  transliteration?: string;
  translation?: string;
  root?: string;
  part_of_speech?: string;
}

export interface AudioSegment {
  word_id: number;
  start_time: number;
  end_time: number;
  audio_url: string;
}