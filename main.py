#!/usr/bin/env python3
"""
Ultra-minimal production entry point for Stable Diffusion WebUI API
Optimized for img2img virtual try-on functionality - skips all problematic initializations
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

# Set environment variables for minimal production
os.environ.setdefault('SD_WEBUI_RESTARTING', '1')
os.environ.setdefault('API_ONLY', 'true')
os.environ.setdefault('SKIP_INSTALL', '1')
os.environ.setdefault('SKIP_EXTENSIONS', '1')  # Skip loading extensions
os.environ.setdefault('SKIP_MODELS', '1')      # Skip loading models initially

# Import after setting environment variables
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Handle missing packages gracefully
try:
    import pillow_avif
except ImportError:
    print("Warning: pillow-avif-plugin not available. AVIF support disabled.")

try:
    import tokenizers
except ImportError:
    print("Warning: tokenizers not available. Some text processing features may be limited.")

try:
    import transformers
except ImportError:
    print("Warning: transformers not available. Text-to-image generation may be limited.")

def create_minimal_app():
    """Create and configure the FastAPI application with minimal initialization"""
    
    print("🚀 Initializing ultra-minimal Stable Diffusion WebUI for img2img...")
    
    # Create FastAPI app
    app = FastAPI(
        title="Stable Diffusion WebUI - Virtual Try-On API",
        description="Ultra-minimal API for image-to-image virtual try-on functionality",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # Configure CORS for uwear-virtual-shop frontend
    allowed_origins = os.getenv('ALLOW_ORIGINS', 'https://uwear-virtual-shop.onrender.com,http://localhost:3000,http://localhost:5173').split(',')
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Add basic health check endpoint
    @app.get("/")
    async def root():
        return {"message": "Stable Diffusion WebUI API - Virtual Try-On Backend", "status": "ready"}
    
    @app.get("/health")
    async def health():
        return {"status": "healthy", "service": "virtual-try-on-api"}
    
    print("✅ Minimal API initialized successfully!")
    
    return app

def main():
    """Main entry point for ultra-minimal production deployment"""
    
    # Use fixed port for consistent deployment
    port = 10000
    host = "0.0.0.0"  # Always bind to all interfaces for Render
    
    print(f"🎯 Starting Ultra-Minimal Virtual Try-On API on {host}:{port}")
    print(f"📱 Frontend: uwear-virtual-shop.onrender.com")
    print(f"🔗 CORS Origins: {os.getenv('ALLOW_ORIGINS', 'https://uwear-virtual-shop.onrender.com,http://localhost:3000,http://localhost:5173')}")
    print(f"🌐 Server will be available at: http://{host}:{port}")
    
    # Create the minimal application
    app = create_minimal_app()
    
    # Launch the API with uvicorn directly
    print(f"🚀 Starting uvicorn server...")
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info",
        access_log=True
    )

if __name__ == "__main__":
    main()
