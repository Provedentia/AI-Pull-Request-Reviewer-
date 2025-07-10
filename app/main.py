from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import uvicorn
from app.routes.webhook import router as webhook_router
from app.core.config import settings
from app.core.logging import setup_logging
import logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="GitHub PR Reviewer",
    description="AI-powered Pull Request reviewer using OpenAI and GitHub APIs",
    version="1.0.0",
    docs_url="/docs" if settings.environment == "development" else None,
    redoc_url="/redoc" if settings.environment == "development" else None
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.environment == "development" else ["https://github.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Add trusted host middleware for production
if settings.environment == "production":
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*"]  # Configure this for your specific domain
    )

# Include routers
app.include_router(webhook_router, prefix="/api/v1")

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with basic information"""
    return {
        "message": "GitHub PR Reviewer API",
        "version": "1.0.0",
        "status": "active",
        "environment": settings.environment
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for deployment platforms"""
    return {
        "status": "healthy",
        "environment": settings.environment
    }

if __name__ == "__main__":
    logger.info(f"Starting GitHub PR Reviewer API on {settings.host}:{settings.port}")
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.environment == "development",
        log_level=settings.log_level.lower()
    )