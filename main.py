"""
Quranic Mushaf View - FastAPI Backend
Main application file with CORS configuration and route setup
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
import uvicorn
import os

from app.routers import mushaf, audio, search, qul_mushaf
from app.database.connection import init_database

# Create FastAPI instance
app = FastAPI(
    title="Quranic Mushaf View API",
    description="Complete Quran API with QUL rendering support and page-specific fonts",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS to allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for frontend-backend interaction
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Mount static files for audio and images
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(mushaf.router, prefix="/api/v1/mushaf", tags=["mushaf"])
app.include_router(audio.router, prefix="/api/v1/audio", tags=["audio"])
app.include_router(search.router, prefix="/api/v1/search", tags=["search"])
app.include_router(qul_mushaf.router, prefix="/api/v1/qul", tags=["qul-mushaf"])

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    await init_database()

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Quranic Mushaf View API",
        "version": "2.0.0",
        "features": [
            "Complete Quran with 83,668 words",
            "QUL rendering system with 604 pages",
            "Page-specific WOFF fonts",
            "Arabic/English UI support",
            "Search functionality",
            "Audio playback support"
        ],
        "endpoints": {
            "qul": "/api/v1/qul/",
            "mushaf": "/api/v1/mushaf/",
            "audio": "/api/v1/audio/",
            "search": "/api/v1/search/"
        }
    }

@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint"""
    # Check if QUL database exists
    qul_db_exists = os.path.exists("app/database/qul_complete.db")
    
    # Check if fonts directory exists
    fonts_exist = os.path.exists("static/fonts") and len(os.listdir("static/fonts")) > 0
    
    return {
        "status": "healthy",
        "qul_database": "available" if qul_db_exists else "missing",
        "fonts": "available" if fonts_exist else "missing",
        "total_pages": 604,
        "font_system": "page-specific"
    }

@app.get("/api/v1/fonts/{page_number}")
async def get_page_font(page_number: int):
    """Get page-specific font file"""
    if page_number < 1 or page_number > 604:
        raise HTTPException(status_code=400, detail="Page number must be between 1 and 604")
    
    font_file = f"static/fonts/p{page_number}.woff"
    
    if not os.path.exists(font_file):
        raise HTTPException(status_code=404, detail=f"Font for page {page_number} not found")
    
    return FileResponse(
        font_file,
        media_type="font/woff",
        headers={"Cache-Control": "public, max-age=31536000"}  # Cache for 1 year
    )

@app.exception_handler(404)
async def not_found_handler(request, exc):
    """Custom 404 handler"""
    return JSONResponse(
        status_code=404,
        content={"message": "Resource not found", "path": str(request.url)}
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    """Custom 500 handler"""
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error", "detail": str(exc)}
    )

if __name__ == "__main__":
    # Run the application
    # Listen on 0.0.0.0 to allow external access
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )

