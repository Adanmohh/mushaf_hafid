# Quranic Mushaf View - Database Schema and Architecture

## 1. Database Schema

We will use a relational database schema to store the Quranic data, Mushaf layouts, and audio timings. The following tables will be created:

### 1.1. `mushaf_layouts`

Stores information about different Mushaf layouts.

| Column          | Type    | Description                                      |
|-----------------|---------|--------------------------------------------------|
| `id`            | Integer | Primary Key                                      |
| `name`          | String  | Name of the Mushaf layout (e.g., "Uthmani Hafs") |
| `total_pages`   | Integer | Total number of pages in the layout              |
| `lines_per_page`| Integer | Number of lines per page                         |
| `font_name`     | String  | Name of the font used for the layout             |

### 1.2. `pages`

Stores information about each page in a Mushaf layout.

| Column             | Type    | Description                               |
|--------------------|---------|-------------------------------------------|
| `id`               | Integer | Primary Key                               |
| `mushaf_layout_id` | Integer | Foreign Key to `mushaf_layouts.id`        |
| `page_number`      | Integer | The page number                           |
| `image_url`        | String  | URL to the page image (for image-based layouts) |

### 1.3. `lines`

Stores information about each line on a page.

| Column      | Type    | Description                      |
|-------------|---------|----------------------------------|
| `id`        | Integer | Primary Key                      |
| `page_id`   | Integer | Foreign Key to `pages.id`        |
| `line_number` | Integer | The line number on the page      |

### 1.4. `words`

Stores information about each word in the Quran.

| Column              | Type    | Description                                      |
|---------------------|---------|--------------------------------------------------|
| `id`                | Integer | Primary Key                                      |
| `line_id`           | Integer | Foreign Key to `lines.id`                        |
| `word_position`     | Integer | Position of the word within the line             |
| `surah_number`      | Integer | Surah number (1-114)                             |
| `ayah_number`       | Integer | Ayah number                                      |
| `word_text_uthmani` | String  | The word in Uthmani script                       |
| `translation_en`    | String  | English translation of the word                  |
| `transliteration_en`| String  | English transliteration of the word              |

### 1.5. `word_positions`

Stores the coordinates of each word on the page for a specific Mushaf layout.

| Column             | Type    | Description                               |
|--------------------|---------|-------------------------------------------|
| `id`               | Integer | Primary Key                               |
| `word_id`          | Integer | Foreign Key to `words.id`                 |
| `mushaf_layout_id` | Integer | Foreign Key to `mushaf_layouts.id`        |
| `page_number`      | Integer | The page number                           |
| `line_number`      | Integer | The line number on the page               |
| `x_coordinate`     | Integer | X-coordinate of the word on the page      |
| `y_coordinate`     | Integer | Y-coordinate of the word on the page      |
| `width`            | Integer | Width of the word                         |
| `height`           | Integer | Height of the word                        |

### 1.6. `recitations`

Stores information about different Quran reciters.

| Column         | Type    | Description                                      |
|----------------|---------|--------------------------------------------------|
| `id`           | Integer | Primary Key                                      |
| `reciter_name` | String  | Name of the reciter                              |
| `style`        | String  | Recitation style (e.g., "Murattal", "Mujawwad") |

### 1.7. `audio_timings`

Stores the word-level audio timings for each recitation.

| Column          | Type    | Description                               |
|-----------------|---------|-------------------------------------------|
| `id`            | Integer | Primary Key                               |
| `word_id`       | Integer | Foreign Key to `words.id`                 |
| `recitation_id` | Integer | Foreign Key to `recitations.id`           |
| `start_time`    | Integer | Start time of the word in milliseconds    |
| `end_time`      | Integer | End time of the word in milliseconds      |
| `audio_file_url`| String  | URL to the audio file for the word        |

## 2. Architecture

We will use a FastAPI backend with the following architecture:

### 2.1. API Endpoints

- **`GET /mushaf/layouts`**: Get a list of available Mushaf layouts.
- **`GET /mushaf/layout/{layout_id}/page/{page_number}`**: Get the data for a specific page of a Mushaf layout, including all words and their positions.
- **`GET /recitations`**: Get a list of available reciters.
- **`GET /recitation/{recitation_id}/word/{word_id}/audio`**: Get the audio for a specific word by a specific reciter.
- **`GET /search?q={query}`**: Search for words in the Quran.

### 2.2. Database Integration

- We will use **SQLAlchemy** as the ORM to interact with the SQLite database.
- We will use **Pydantic** models for data validation and serialization.

### 2.3. Audio Serving

- Audio files will be served through the FastAPI backend.
- The `audio_timings` table will be used to provide word-level audio synchronization.

### 2.4. Frontend Integration

- The FastAPI backend will expose a RESTful API that can be consumed by any frontend framework (e.g., React, Vue.js, Svelte).
- The frontend will be responsible for rendering the Mushaf view and handling user interactions.


