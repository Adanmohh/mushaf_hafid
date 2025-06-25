"""
Quranic Mushaf View - FastAPI Backend
Main application file with CORS configuration and route setup
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import uvicorn
import os

from app.routers import mushaf, audio, search, qul_mushaf
from app.database.connection import init_database

# Create FastAPI instance
app = FastAPI(
    title="Quranic Mushaf API",
    description="A comprehensive API for Quranic Mushaf view with word-level audio synchronization",
    version="1.0.0",
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
        "message": "Quranic Mushaf API",
        "version": "1.0.0",
        "description": "A comprehensive API for Quranic Mushaf view with word-level audio synchronization",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "API is running"}

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

