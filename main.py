#!/usr/bin/env python3
"""
Virtual Try-On API for Stable Diffusion WebUI
Minimal version for Render starter plan compatibility
"""

import os
import sys
import base64
import io
import time
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

# Basic Image Processing (PIL only)
try:
    from PIL import Image, ImageDraw, ImageFilter
    import numpy as np
    IMAGE_PROCESSING_AVAILABLE = True
    print("✅ PIL and basic image processing available")
except ImportError as e:
    IMAGE_PROCESSING_AVAILABLE = False
    print(f"⚠️ Image processing not available: {e}")

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
    try:
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Save to bytes
        buffer = io.BytesIO()
        image.save(buffer, format='PNG')
        buffer.seek(0)
        
        # Encode to base64
        image_bytes = buffer.getvalue()
        base64_string = base64.b64encode(image_bytes).decode('utf-8')
        
        return base64_string
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Image encoding failed: {str(e)}")

def process_virtual_try_on(
    person_image: Image.Image,
    clothing_image: Image.Image,
    prompt: str = "person wearing the clothing, high quality, detailed",
    negative_prompt: str = "blurry, low quality, distorted",
    strength: float = 0.75,
    guidance_scale: float = 7.5,
    steps: int = 20
) -> Image.Image:
    """
    Process virtual try-on using basic image processing
    This is a placeholder implementation - real AI processing would be added later
    """
    
    if not IMAGE_PROCESSING_AVAILABLE:
        raise Exception("Image processing not available")
    
    try:
        # Convert images to RGB
        person_img = person_image.convert('RGB')
        clothing_img = clothing_image.convert('RGB')
        
        # Resize clothing to fit person (simple approach)
        person_width, person_height = person_img.size
        clothing_width, clothing_height = clothing_img.size
        
        # Calculate scaling factor to fit clothing on person
        scale_factor = min(person_width / clothing_width * 0.8, person_height / clothing_height * 0.6)
        new_clothing_width = int(clothing_width * scale_factor)
        new_clothing_height = int(clothing_height * scale_factor)
        
        # Resize clothing
        clothing_resized = clothing_img.resize((new_clothing_width, new_clothing_height), Image.Resampling.LANCZOS)
        
        # Create a copy of person image
        result = person_img.copy()
        
        # Calculate position to overlay clothing (center it on the person)
        x_offset = (person_width - new_clothing_width) // 2
        y_offset = (person_height - new_clothing_height) // 2
        
        # Create a mask for the clothing (simple approach)
        clothing_mask = clothing_resized.convert('RGBA')
        
        # Apply some basic blending
        if clothing_mask.mode == 'RGBA':
            # Use alpha channel for blending
            result.paste(clothing_mask, (x_offset, y_offset), clothing_mask)
        else:
            # Simple overlay without alpha
            result.paste(clothing_resized, (x_offset, y_offset))
        
        return result
        
    except Exception as e:
        raise Exception(f"Virtual try-on processing failed: {str(e)}")

def create_virtual_tryon_app():
    """Create and configure the FastAPI application with virtual try-on endpoints"""
    
    print("🚀 Initializing Virtual Try-On API...")
    
    app = FastAPI(
        title="Stable Diffusion WebUI - Virtual Try-On API",
        description="Virtual try-on API for image-to-image clothing fitting (Minimal Version)",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # Configure CORS
    origins = os.getenv('ALLOW_ORIGINS', 'https://uwear-virtual-shop.onrender.com,http://localhost:3000,http://localhost:5173').split(',')
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    @app.get("/")
    async def root():
        return {
            "message": "Stable Diffusion WebUI API - Virtual Try-On Backend (Minimal Version)",
            "status": "ready",
            "image_processing_available": IMAGE_PROCESSING_AVAILABLE,
            "note": "This is a minimal version for Render starter plan. Real AI processing will be added in Phase 4."
        }
    
    @app.get("/health")
    async def health():
        return {
            "status": "healthy",
            "service": "virtual-try-on-api",
            "capabilities": {
                "image_processing": IMAGE_PROCESSING_AVAILABLE,
                "stable_diffusion": False,  # Not available in minimal version
                "ai_processing": False      # Not available in minimal version
            },
            "version": "1.0.0-minimal"
        }
    
    @app.post("/api/virtual-tryon", response_model=VirtualTryOnResponse)
    async def virtual_tryon(request: VirtualTryOnRequest):
        """Virtual try-on endpoint using basic image processing"""
        
        if not IMAGE_PROCESSING_AVAILABLE:
            return VirtualTryOnResponse(
                success=False,
                message="Image processing not available"
            )
        
        start_time = time.time()
        
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
            
            processing_time = time.time() - start_time
            
            return VirtualTryOnResponse(
                success=True,
                result_image=result_base64,
                message="Virtual try-on completed successfully (basic overlay)",
                processing_time=processing_time
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
        
        if not IMAGE_PROCESSING_AVAILABLE:
            raise HTTPException(status_code=503, detail="Image processing not available")
        
        try:
            # Read uploaded files
            person_img = Image.open(io.BytesIO(await person_image.read()))
            clothing_img = Image.open(io.BytesIO(await clothing_image.read()))
            
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
                "message": "Test virtual try-on completed (basic overlay)"
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
    print(f"⚠️ This is a minimal version for Render starter plan compatibility")
    
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
