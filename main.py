#!/usr/bin/env python3
"""
Streamlined production entry point for Stable Diffusion WebUI API
Optimized for img2img virtual try-on functionality
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

# Set environment variables for production
os.environ.setdefault('SD_WEBUI_RESTARTING', '1')
os.environ.setdefault('API_ONLY', 'true')
os.environ.setdefault('SKIP_INSTALL', '1')  # Skip some installations for faster startup

# Import after setting environment variables
from modules import initialize_util, initialize
from modules.shared_cmd_options import cmd_opts
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

def create_streamlined_app():
    """Create and configure the FastAPI application optimized for img2img"""
    
    print("🚀 Initializing streamlined Stable Diffusion WebUI for img2img...")
    
    # Initialize the Stable Diffusion WebUI with minimal components
    initialize.initialize()
    
    # Create FastAPI app
    app = FastAPI(
        title="Stable Diffusion WebUI - Virtual Try-On API",
        description="Streamlined API for image-to-image virtual try-on functionality",
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
    
    # Setup Stable Diffusion WebUI middleware
    initialize_util.setup_middleware(app)
    
    # Create and register the API
    from modules.api.api import Api
    from modules.call_queue import queue_lock
    
    api = Api(app, queue_lock)
    
    # Register minimal callbacks for img2img functionality
    from modules import script_callbacks
    script_callbacks.before_ui_callback()
    script_callbacks.app_started_callback(None, app)
    
    print("✅ Streamlined API initialized successfully!")
    
    return app, api

def main():
    """Main entry point for streamlined production deployment"""
    
    # Get port from environment or use default
    port = int(os.getenv('PORT', 10000))
    host = os.getenv('GRADIO_SERVER_NAME', '0.0.0.0')
    
    print(f"🎯 Starting Virtual Try-On API on {host}:{port}")
    print(f"📱 Frontend: uwear-virtual-shop.onrender.com")
    print(f"🔗 CORS Origins: {os.getenv('ALLOW_ORIGINS', 'https://uwear-virtual-shop.onrender.com,http://localhost:3000,http://localhost:5173')}")
    
    # Create the streamlined application
    app, api = create_streamlined_app()
    
    # Launch the API
    api.launch(
        server_name=host,
        port=port,
        root_path=""
    )

if __name__ == "__main__":
    main()
