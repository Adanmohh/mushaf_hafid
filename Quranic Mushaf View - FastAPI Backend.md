# Quranic Mushaf View - FastAPI Backend

A comprehensive FastAPI backend for displaying the Quran in traditional Mushaf format with word-level audio synchronization.

## Features

- **Word-Level Database Organization**: Precise word positioning and layout data
- **Multiple Mushaf Layouts**: Support for different Mushaf styles (Uthmani, IndoPak, etc.)
- **Audio Integration**: Word-level audio timing for synchronized recitation
- **Search Functionality**: Advanced search across Arabic text, translations, and transliterations
- **RESTful API**: Clean, documented API endpoints
- **CORS Support**: Ready for frontend integration
- **Responsive Design Ready**: Optimized for both desktop and mobile clients

## Project Structure

```
quran_mushaf_api/
├── app/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── database.py          # SQLAlchemy models
│   │   └── mushaf.py            # Pydantic models
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── mushaf.py            # Mushaf layout endpoints
│   │   ├── audio.py             # Audio and recitation endpoints
│   │   └── search.py            # Search endpoints
│   ├── services/
│   │   └── __init__.py
│   └── database/
│       ├── __init__.py
│       ├── connection.py        # Database connection and setup
│       └── quran.db            # SQLite database (created on first run)
├── static/
│   ├── audio/                   # Audio files directory
│   └── images/                  # Mushaf page images directory
├── tests/                       # Test files
├── main.py                      # FastAPI application entry point
├── init_db.py                   # Database initialization script
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## Installation

1. **Clone or download the project**:
   ```bash
   cd quran_mushaf_api
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize the database**:
   ```bash
   python init_db.py
   ```

4. **Run the application**:
   ```bash
   python main.py
   ```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:
- **Interactive API docs**: http://localhost:8000/docs
- **ReDoc documentation**: http://localhost:8000/redoc

## API Endpoints

### Mushaf Layouts

- `GET /api/v1/mushaf/layouts` - Get all available Mushaf layouts
- `GET /api/v1/mushaf/layout/{layout_id}` - Get specific layout details
- `GET /api/v1/mushaf/layout/{layout_id}/page/{page_number}` - Get complete page data
- `GET /api/v1/mushaf/layout/{layout_id}/pages` - Get page range
- `GET /api/v1/mushaf/surah/{surah_number}/ayah/{ayah_number}/page` - Find ayah location

### Audio & Recitations

- `GET /api/v1/audio/recitations` - Get all available recitations
- `GET /api/v1/audio/recitation/{recitation_id}` - Get recitation details
- `GET /api/v1/audio/word/{word_id}/recitation/{recitation_id}` - Get word audio timing
- `GET /api/v1/audio/ayah/{surah}/{ayah}/recitation/{recitation_id}` - Get ayah audio with timings
- `GET /api/v1/audio/file/{filename}` - Serve audio files
- `GET /api/v1/audio/surah/{surah}/recitation/{recitation_id}/timings` - Get surah timings
- `GET /api/v1/audio/stats/recitation/{recitation_id}` - Get recitation statistics

### Search

- `GET /api/v1/search/?q={query}` - Search Quran text
- `GET /api/v1/search/suggestions?q={query}` - Get search suggestions
- `GET /api/v1/search/ayah/{surah}/{ayah}?q={query}` - Search within specific ayah
- `GET /api/v1/search/advanced` - Advanced search with multiple criteria

## Database Schema

The database consists of the following main tables:

- **mushaf_layouts**: Different Mushaf layout configurations
- **pages**: Page information for each layout
- **lines**: Line organization within pages
- **words**: Individual words with Arabic text and translations
- **word_positions**: Precise positioning coordinates for each word
- **recitations**: Available reciters and their styles
- **audio_timings**: Word-level audio timing data

## Data Sources

This implementation is designed to work with data from:

1. **QUL (Quranic Universal Library)**: Mushaf layout data and positioning
2. **EveryAyah**: Audio files and recitations
3. **Quran-align project**: Word-level audio timing data
4. **Tanzil**: Quranic text and translations

## Configuration

### CORS Settings
The API is configured to allow all origins by default for development. For production, modify the CORS settings in `main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # Specify allowed origins
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)
```

### Database Configuration
The default database is SQLite stored in `app/database/quran.db`. For production, you can modify the database URL in `app/database/connection.py`.

## Sample Data

The application includes sample data for Al-Fatiha (first chapter) to demonstrate functionality:
- Sample Mushaf layout (Uthmani Hafs)
- Sample words with positions
- Sample audio timings
- Sample recitation (Abdul Basit Abdul Samad)

## Adding Real Data

To populate the database with complete Quranic data:

1. **Download Mushaf layout data** from QUL in SQLite format
2. **Download audio files** and timing data from quran-align project
3. **Import the data** using custom scripts or database tools
4. **Update file paths** in the database to match your static file structure

## Frontend Integration

This API is designed to work with any frontend framework. Key integration points:

1. **Page Display**: Use `/mushaf/layout/{id}/page/{num}` to get word positions
2. **Audio Sync**: Use word timing data to highlight words during playback
3. **Search**: Implement search with suggestions and advanced filters
4. **Navigation**: Use ayah location endpoints for quick navigation

## Performance Considerations

- **Indexing**: Database includes indexes on frequently queried columns
- **Pagination**: Search and list endpoints support pagination
- **Caching**: Consider implementing Redis for frequently accessed data
- **CDN**: Use CDN for serving audio files and images in production

## Development

### Running in Development Mode
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Running Tests
```bash
pytest tests/
```

### Code Style
The project follows PEP 8 guidelines. Use tools like `black` and `flake8` for code formatting.

## Deployment

### Using Docker
Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Using Cloud Platforms
The application is ready for deployment on:
- **Heroku**: Add `Procfile` with `web: uvicorn main:app --host 0.0.0.0 --port $PORT`
- **AWS Lambda**: Use Mangum adapter for serverless deployment
- **Google Cloud Run**: Use the Docker approach
- **DigitalOcean App Platform**: Direct deployment from Git repository

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is open source. Please respect the licenses of the data sources used (QUL, EveryAyah, etc.).

## Acknowledgments

- **QUL (Quranic Universal Library)** for Mushaf layout data
- **Quran-align project** for word-level audio timing techniques
- **EveryAyah** for audio recitation resources
- **Quran.com** and **open-mushaf** for implementation inspiration

## Support

For questions or issues, please create an issue in the project repository or refer to the API documentation at `/docs` endpoint.

