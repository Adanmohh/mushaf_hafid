# QUL Resources Analysis - Initial Findings

## Key Resources for Mushaf Implementation

### 1. Mushaf layouts (25 resources)
- **Description**: Download Mushaf layout data to render Quran pages exactly like the printed Mushaf
- **Details**: 20 Layouts (Approved), 5 Layouts (WIP)
- **Importance**: Critical for accurate page layout and word positioning

### 2. Recitations and segments data (148 resources)
- **Description**: High-quality audio files with detailed timestamp data for ayah-by-ayah and surah-by-surah
- **Details**: 87 Unsegmented Audio, 61 Segmented Audio
- **Importance**: Essential for audio integration and word-level synchronization

### 3. Translations (204 resources)
- **Description**: Ayah by ayah and word by word translations in different languages
- **Details**: 189 Translations, 15 Word by word translations
- **Importance**: For multi-language support

### 4. Quran script: Unicode & Images (26 resources)
- **Description**: Quran script in Unicode text or image formats (Madani, IndoPak, Uthmani scripts)
- **Importance**: For text rendering and display

### 5. Quran Fonts (17 resources)
- **Description**: Quran-related fonts including glyph-based, Unicode, and translation fonts
- **Details**: Indopak, Madani fonts with specialized fonts for Surah names and headings
- **Importance**: For proper Arabic text rendering

### 6. Quran metadata (8 resources)
- **Description**: Surah, ayah, juz, hizb, rub, manzil metadata
- **Importance**: For navigation and organization

### 7. Tafsirs (106 resources)
- **Description**: Tafsir data in multiple languages with ayah grouping information
- **Details**: 32 Mukhtasar tafsirs, 74 Detailed tafsirs
- **Importance**: For commentary and explanation features

## Key Insights
- QUL provides comprehensive data resources but no API (download and package approach)
- Mushaf layouts are specifically designed to match printed Mushaf appearance
- Audio data includes timestamp information for word-level synchronization
- Multiple script formats available (Unicode, images)
- Resources are available in SQLite and JSON formats



## Mushaf Layout Tool Analysis

### Key Findings from QUL Mushaf Layout Tool:

1. **Layout Structure**:
   - Uthmani Hafs layout: 604 pages, 15 lines per page
   - Uses "me_quran" font for Arabic text
   - Each word has precise positioning coordinates
   - Words are numbered sequentially for reference

2. **Word-Level Organization**:
   - Each word is individually positioned with exact coordinates
   - Words are organized into lines, lines into pages
   - Page 1 contains Ayahs 1:1 - 1:7 (Al-Fatiha)
   - Visual representation shows word boundaries and positioning

3. **Database Structure Implications**:
   - Need tables for: Pages, Lines, Words, Positions
   - Each word should have: page_number, line_number, word_position, coordinates
   - Font size and styling information per layout
   - Ayah and Surah references for each word

4. **Layout Tool Features**:
   - Adjustable pages, lines per page, alignment
   - Word placement precision for accurate Mushaf representation
   - Multiple layout options (Uthmani, Indopak, QPC, etc.)
   - Font size controls and styling options

### Available Mushaf Layouts:
- QCF V2 (1421H print): 604 pages, 15 lines, v2 font
- Quran Complex V1 (1405 print): 604 pages, 15 lines, v1 font
- Indopak (pdms font): 604 pages, 15 lines, indopak font
- Uthmani Hafs: 604 pages, 15 lines, me_quran font
- KFGQPC HAFS: 604 pages, 15 lines, qpc-hafs font
- Various Indopak layouts with different line counts (14-16 lines)


## Open-Mushaf Project Analysis

### Project Overview:
- **Technology Stack**: TypeScript, Next.js, PWA, TailwindCSS
- **Live Demo**: open-mushaf.vercel.app
- **License**: MIT License
- **Repository**: https://github.com/adelpro/open-mushaf

### Key Resources Used:
1. **Mushaf Pages**: From the Quran Complex of King Fehd
2. **Database**: JSON format from Mushaf-mauri project
3. **Tafseer Data**: From Ayat project
4. **Icons**: From SVGRepo

### Features:
- Offline access to Quran Mushaf pages
- Responsive design for desktop and mobile
- Multiple Tafseer (exegesis) options
- Smooth navigation between Surahs and Juz
- High-quality images from King Fehd Complex

### Technical Implementation Insights:
- Uses JSON database format (not SQLite)
- PWA implementation for offline access
- Image-based Mushaf pages (not text-based layout)
- Next.js for frontend framework
- Serwist for PWA functionality

### Comparison with QUL Approach:
- **QUL**: Word-level positioning data, SQLite database, precise layout control
- **Open-Mushaf**: Image-based pages, JSON database, simpler implementation
- **QUL**: More suitable for word-level audio synchronization
- **Open-Mushaf**: Better for quick deployment and offline access


## Quran-Align Project Analysis

### Project Overview:
- **Purpose**: Word-precise segmentation of recorded Quranic recitation
- **Repository**: https://github.com/cpfair/quran-align
- **Stars**: 216 stars, 39 forks
- **Language**: C++ (94.7%), Python (2.2%)
- **License**: MIT License

### Key Features:
- Produces word-accurate timestamps for Quranic audio
- Designed to work with EveryAyah style audio input
- Each word gets precise start and end timestamp within recorded audio
- Can be used for:
  - Word highlighting during playback
  - Repeating specific words or phrases
  - Comparing against other audio
  - Analyzing qari's speaking cadence

### Data Availability:
- Pre-generated word-by-word timing files available
- Licensed under Creative Commons Attribution 4.0 International License
- Can download from Releases tab without running the tool

### Technical Implementation:
- Uses speech recognition and audio processing
- C++ based for performance
- Outputs timing data that can be integrated into web applications
- Compatible with EveryAyah audio format

### Integration Potential for Our FastAPI Backend:
- Can use pre-generated timing files as database source
- Perfect for word-level audio synchronization
- Enables precise highlighting of words during recitation
- Supports multiple reciters if timing data available

