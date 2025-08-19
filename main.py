#!/usr/bin/env python3
"""
Virtual Try-On API for Stable Diffusion WebUI
Phase 1: Basic Image Processing + Phase 2: Stable Diffusion Core + Phase 3: API Endpoints
"""

import os
import sys
import base64
import io
from pathlib import Path
from typing import Optional

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

# Set environment variables for minimal production
os.environ.setdefault('SD_WEBUI_RESTARTING', '1')
os.environ.setdefault('API_ONLY', 'true')
os.environ.setdefault('SKIP_INSTALL', '1')
os.environ.setdefault('SKIP_EXTENSIONS', '1')  # Skip loading extensions
os.environ.setdefault('SKIP_MODELS', '1')      # Skip loading models initially

# Import after setting environment variables
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from pydantic import BaseModel

# Phase 1: Basic Image Processing
try:
    import torch
    import torchvision.transforms as transforms
    from PIL import Image
    import numpy as np
    TORCH_AVAILABLE = True
    print("✅ PyTorch and image processing available")
except ImportError as e:
    TORCH_AVAILABLE = False
    print(f"⚠️ PyTorch not available: {e}")

# Phase 2: Stable Diffusion Core
try:
    import safetensors
    import einops
    import omegaconf
    SD_CORE_AVAILABLE = True
    print("✅ Stable Diffusion core components available")
except ImportError as e:
    SD_CORE_AVAILABLE = False
    print(f"⚠️ Stable Diffusion core not available: {e}")

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

# Pydantic models for API
class VirtualTryOnRequest(BaseModel):
    person_image: str  # Base64 encoded image
    clothing_image: str  # Base64 encoded image
    prompt: Optional[str] = "person wearing the clothing, high quality, detailed"
    negative_prompt: Optional[str] = "blurry, low quality, distorted"
    strength: Optional[float] = 0.75
    guidance_scale: Optional[float] = 7.5
    steps: Optional[int] = 20

class VirtualTryOnResponse(BaseModel):
    success: bool
    result_image: Optional[str] = None  # Base64 encoded result
    message: str
    processing_time: Optional[float] = None

def decode_base64_to_image(base64_string: str) -> Image.Image:
    """Decode base64 string to PIL Image"""
    try:
        # Remove data URL prefix if present
        if base64_string.startswith('data:image'):
            base64_string = base64_string.split(',')[1]
        
        image_data = base64.b64decode(base64_string)
        image = Image.open(io.BytesIO(image_data))
        return image
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image data: {str(e)}")

def encode_image_to_base64(image: Image.Image) -> str:
    """Encode PIL Image to base64 string"""
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return img_str

def process_virtual_try_on(person_image: Image.Image, clothing_image: Image.Image, 
                          prompt: str, negative_prompt: str, strength: float, 
                          guidance_scale: float, steps: int) -> Image.Image:
    """
    Process virtual try-on (simplified version for now)
    This is a placeholder that will be enhanced with actual Stable Diffusion logic
    """
    import time
    start_time = time.time()
    
    # For now, return a simple overlay as placeholder
    # In the full implementation, this would use Stable Diffusion img2img
    
    # Resize images to same size
    target_size = (512, 512)
    person_resized = person_image.resize(target_size, Image.Resampling.LANCZOS)
    clothing_resized = clothing_image.resize(target_size, Image.Resampling.LANCZOS)
    
    # Simple overlay (placeholder for actual AI processing)
    result = person_resized.copy()
    result.paste(clothing_resized, (0, 0), clothing_resized.convert('RGBA'))
    
    processing_time = time.time() - start_time
    print(f"Virtual try-on processing time: {processing_time:.2f}s")
    
    return result

def create_virtual_tryon_app():
    """Create and configure the FastAPI application with virtual try-on endpoints"""
    
    print("🚀 Initializing Virtual Try-On API...")
    
    # Create FastAPI app
    app = FastAPI(
        title="Stable Diffusion WebUI - Virtual Try-On API",
        description="Virtual try-on API for image-to-image clothing fitting",
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
    
    # Health check endpoint
    @app.get("/")
    async def root():
        return {
            "message": "Stable Diffusion WebUI API - Virtual Try-On Backend", 
            "status": "ready",
            "torch_available": TORCH_AVAILABLE,
            "sd_core_available": SD_CORE_AVAILABLE
        }
    
    @app.get("/health")
    async def health():
        return {
            "status": "healthy", 
            "service": "virtual-try-on-api",
            "capabilities": {
                "image_processing": TORCH_AVAILABLE,
                "stable_diffusion": SD_CORE_AVAILABLE
            }
        }
    
    # Virtual try-on endpoint
    @app.post("/api/virtual-tryon", response_model=VirtualTryOnResponse)
    async def virtual_tryon(request: VirtualTryOnRequest):
        """Main virtual try-on endpoint"""
        
        if not TORCH_AVAILABLE:
            raise HTTPException(status_code=503, detail="Image processing not available")
        
        try:
            # Decode images
            person_image = decode_base64_to_image(request.person_image)
            clothing_image = decode_base64_to_image(request.clothing_image)
            
            # Process virtual try-on
            result_image = process_virtual_try_on(
                person_image=person_image,
                clothing_image=clothing_image,
                prompt=request.prompt,
                negative_prompt=request.negative_prompt,
                strength=request.strength,
                guidance_scale=request.guidance_scale,
                steps=request.steps
            )
            
            # Encode result
            result_base64 = encode_image_to_base64(result_image)
            
            return VirtualTryOnResponse(
                success=True,
                result_image=result_base64,
                message="Virtual try-on completed successfully",
                processing_time=0.5  # Placeholder
            )
            
        except Exception as e:
            return VirtualTryOnResponse(
                success=False,
                message=f"Virtual try-on failed: {str(e)}"
            )
    
    # File upload endpoint for testing
    @app.post("/api/upload-test")
    async def upload_test(person_image: UploadFile = File(...), clothing_image: UploadFile = File(...)):
        """Test endpoint for file uploads"""
        
        if not TORCH_AVAILABLE:
            raise HTTPException(status_code=503, detail="Image processing not available")
        
        try:
            # Read uploaded files
            person_img = Image.open(io.BytesIO(await person_image.read()))
            clothing_img = Image.open(io.BytesIO(await clothing_image.read()))
            
            # Convert to base64 for processing
            person_base64 = encode_image_to_base64(person_img)
            clothing_base64 = encode_image_to_base64(clothing_img)
            
            # Process virtual try-on
            result_image = process_virtual_try_on(
                person_image=person_img,
                clothing_image=clothing_img,
                prompt="person wearing the clothing, high quality, detailed",
                negative_prompt="blurry, low quality, distorted",
                strength=0.75,
                guidance_scale=7.5,
                steps=20
            )
            
            # Return result
            result_base64 = encode_image_to_base64(result_image)
            
            return {
                "success": True,
                "result_image": result_base64,
                "message": "Test virtual try-on completed"
            }
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")
    
    print("✅ Virtual Try-On API initialized successfully!")
    
    return app

def main():
    """Main entry point for virtual try-on API deployment"""
    
    # Use fixed port for consistent deployment
    port = 10000
    host = "0.0.0.0"  # Always bind to all interfaces for Render
    
    print(f"🎯 Starting Virtual Try-On API on {host}:{port}")
    print(f"📱 Frontend: uwear-virtual-shop.onrender.com")
    print(f"🔗 CORS Origins: {os.getenv('ALLOW_ORIGINS', 'https://uwear-virtual-shop.onrender.com,http://localhost:3000,http://localhost:5173')}")
    print(f"🌐 Server will be available at: http://{host}:{port}")
    print(f"📚 API Documentation: http://{host}:{port}/docs")
    
    # Create the virtual try-on application
    app = create_virtual_tryon_app()
    
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
