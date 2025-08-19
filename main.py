#!/usr/bin/env python3
"""
Production-ready main entry point for Stable Diffusion WebUI API
Configured for Render deployment as backend for uwear-virtual-shop
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

# Set environment variables for production
os.environ.setdefault('SD_WEBUI_RESTARTING', '1')
os.environ.setdefault('API_ONLY', 'true')

# Import after setting environment variables
from modules import initialize_util, initialize
from modules.shared_cmd_options import cmd_opts
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Handle missing pillow-avif-plugin gracefully
try:
    import pillow_avif
except ImportError:
    print("Warning: pillow-avif-plugin not available. AVIF support disabled.")

def create_production_app():
    """Create and configure the FastAPI application for production"""
    
    # Initialize the Stable Diffusion WebUI
    initialize.initialize()
    
    # Create FastAPI app
    app = FastAPI(
        title="Stable Diffusion WebUI API",
        description="Production API for Stable Diffusion WebUI - Backend for uwear-virtual-shop",
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
    
    # Register callbacks
    from modules import script_callbacks
    script_callbacks.before_ui_callback()
    script_callbacks.app_started_callback(None, app)
    
    return app, api

def main():
    """Main entry point for production deployment"""
    
    # Get port from environment or use default
    port = int(os.getenv('PORT', 10000))
    host = os.getenv('GRADIO_SERVER_NAME', '0.0.0.0')
    
    print(f"Starting Stable Diffusion WebUI API on {host}:{port}")
    print(f"Environment: Production")
    print(f"CORS Origins: {os.getenv('ALLOW_ORIGINS', 'https://uwear-virtual-shop.onrender.com,http://localhost:3000,http://localhost:5173')}")
    
    # Create the application
    app, api = create_production_app()
    
    # Launch the API
    api.launch(
        server_name=host,
        port=port,
        root_path=""
    )

if __name__ == "__main__":
    main()
