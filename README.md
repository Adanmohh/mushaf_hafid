# Mushaf Hafid - Interactive Quranic Mushaf View

A modern, interactive Quranic Mushaf application with word-level audio synchronization, built with FastAPI backend and React TypeScript frontend.

## 🌟 Features

- **Interactive Mushaf View**: Click on any word to see translation and transliteration
- **Word-Level Audio**: Synchronized audio playback with word highlighting
- **Search Functionality**: Search Arabic text, translations, and transliterations
- **Page Navigation**: Easy navigation between pages and direct ayah lookup
- **Responsive Design**: Modern, clean UI with Arabic font support
- **RESTful API**: Complete backend with comprehensive endpoints

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│            React Frontend              │
│        (TypeScript + Vite)             │
└─────────────┬───────────────────────────┘
              │ HTTP/REST API
┌─────────────▼───────────────────────────┐
│           FastAPI Backend              │
│     (Python + SQLAlchemy)              │
└─────────────┬───────────────────────────┘
              │ SQLite Database
┌─────────────▼───────────────────────────┐
│          Database Layer                │
│   (Word positions, Audio timings)      │
└─────────────────────────────────────────┘
```

## 📋 Prerequisites

- **Python 3.8+** with pip
- **Node.js 16+** with npm
- **Modern web browser** with JavaScript enabled

## 🚀 Quick Start

### 1. Clone and Setup
```bash
cd mushaf_hafid
python3 setup.py --install-deps
```

### 2. Start Backend Server
```bash
python3 main.py
```
Backend will be available at: http://localhost:8000

### 3. Start Frontend Development Server
```bash
cd frontend
npm run dev
```
Frontend will be available at: http://localhost:5173

### 4. Access the Application
Open your browser and navigate to: **http://localhost:5173**

## 🎯 Usage

### Basic Navigation
- **Page Navigation**: Use the Previous/Next buttons or enter a page number
- **Ayah Navigation**: Enter Surah and Ayah numbers to jump directly to any verse
- **Word Interaction**: Click any word to see its translation and transliteration

### Audio Features
- **Double-click any word** to load and play the complete ayah audio
- **Single-click the play button** to start/pause audio playback
- **Click on individual words** in Word Info panel to play word-specific audio
- **Progress bar** shows current playback position with click-to-seek functionality

### Search Features
- **Text Search**: Search for Arabic text, English translations, or transliterations
- **Real-time Results**: See search suggestions and results instantly
- **Navigation**: Click on search results to navigate directly to that ayah

## 🔧 API Endpoints

### Mushaf Endpoints
- `GET /api/v1/mushaf/layouts` - Get available layouts
- `GET /api/v1/mushaf/layout/{id}/page/{num}` - Get page with word positions
- `GET /api/v1/mushaf/surah/{surah}/ayah/{ayah}/page` - Find ayah location

### Audio Endpoints
- `GET /api/v1/audio/recitations` - Get available reciters
- `GET /api/v1/audio/word/{word_id}/recitation/{rec_id}` - Get word timing
- `GET /api/v1/audio/ayah/{surah}/{ayah}/recitation/{rec_id}` - Get ayah audio

### Search Endpoints
- `GET /api/v1/search/?q={query}` - Search Quran text
- `GET /api/v1/search/suggestions?q={query}` - Get search suggestions

## 📊 Database Schema

The application uses SQLite with the following key tables:

- **mushaf_layouts**: Different Mushaf configurations
- **pages**: Page information for each layout  
- **lines**: Line organization within pages
- **words**: Individual words with Arabic text and translations
- **word_positions**: Precise X,Y coordinates for each word
- **recitations**: Available reciters and styles
- **audio_timings**: Word-level audio synchronization data

## 🎨 Frontend Technology Stack

- **React 18** with TypeScript
- **Vite** for fast development and building
- **Custom CSS** with responsive design
- **Axios** for API communication
- **Custom hooks** for state management

## 🔍 Sample Data

The application comes with sample data for **Al-Fatiha (Chapter 1)** including:
- Complete word positioning data
- Translation and transliteration for each word
- Mock audio timing data
- Proper Arabic text rendering

## 📝 Development

### Project Structure
```
mushaf_hafid/
├── app/                    # Backend application
│   ├── routers/           # API route handlers
│   ├── models/            # Pydantic models
│   └── database/          # Database configuration
├── frontend/              # React frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── hooks/         # Custom React hooks
│   │   ├── services/      # API service layer
│   │   └── types/         # TypeScript type definitions
│   └── public/            # Static assets
├── static/                # Backend static files
├── main.py               # FastAPI application entry point
├── init_db.py            # Database initialization
└── sample_data.py        # Sample data insertion
```

### Adding New Features

1. **Backend**: Add new routes in `app/routers/`
2. **Frontend**: Create new components in `src/components/`
3. **Database**: Modify `database.py` and `init_db.py`
4. **API Integration**: Update `src/services/api.ts`

## 🔒 Security Features

- **CORS Configuration**: Properly configured for frontend-backend communication
- **Input Validation**: Pydantic models ensure data integrity
- **Error Handling**: Comprehensive error handling throughout the application
- **Rate Limiting**: Ready for production rate limiting implementation

## 📈 Performance Optimizations

- **Database Indexing**: Optimized indexes for fast queries
- **Async Operations**: Fully async backend for high performance
- **Efficient Frontend**: React hooks prevent unnecessary re-renders
- **Lazy Loading**: Components and data loaded as needed

## 🛠️ Troubleshooting

### Backend Issues
- **Database not found**: Run `python3 init_db.py` and `python3 sample_data.py`
- **Port conflicts**: Change port in `main.py` (default: 8000)
- **CORS errors**: Check `main.py` CORS configuration

### Frontend Issues
- **API connection**: Ensure backend is running on port 8000
- **Build errors**: Run `npm install` in frontend directory
- **Port conflicts**: Vite dev server uses port 5173 by default

### Common Issues
- **Python dependencies**: Install with `python3 -m pip install -r requirements.txt`
- **Node dependencies**: Install with `npm install` in frontend directory

## 📄 API Documentation

Full API documentation is available at: **http://localhost:8000/docs** (Swagger UI)

Alternative documentation: **http://localhost:8000/redoc** (ReDoc)

## 🌍 Future Enhancements

- **Multiple Layouts**: Support for different Mushaf styles (IndoPak, etc.)
- **Real Audio Files**: Integration with actual Quranic recitation files
- **Bookmark System**: Save favorite verses and notes
- **Offline Support**: Progressive Web App capabilities
- **Multi-language**: Additional translation languages
- **Social Features**: Share verses and annotations

## 📞 Support

For questions, issues, or contributions:
1. Check the troubleshooting section above
2. Review API documentation at `/docs`
3. Examine the sample data structure
4. Test with provided Al-Fatiha data

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📜 License

This project is intended for educational and religious purposes. Please ensure proper attribution when using or extending this codebase.

---

**Built with ❤️ for the Muslim community**