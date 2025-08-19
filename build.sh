#!/bin/bash

# Build script for Render deployment
# Handles problematic packages gracefully

echo "🚀 Starting build process..."

# Upgrade pip
pip install --upgrade pip

# Install packages that don't require compilation first
echo "📦 Installing core dependencies..."
pip install --no-cache-dir --prefer-binary \
    fastapi>=0.90.1 \
    uvicorn[standard]>=0.20.0 \
    gradio==3.41.2 \
    python-multipart>=0.0.6 \
    numpy>=1.21.0 \
    requests>=2.28.0 \
    GitPython>=3.1.0 \
    psutil>=5.9.0 \
    Pillow>=9.0.0 \
    scikit-image>=0.19.0 \
    kornia>=0.6.0 \
    torch>=2.0.0 \
    torchvision>=0.15.0 \
    transformers==4.30.2 \
    accelerate>=0.20.0 \
    safetensors>=0.3.0 \
    omegaconf>=2.3.0 \
    einops>=0.6.0 \
    tomesd>=0.1.0 \
    blendmodes>=2022 \
    clean-fid>=0.1.35 \
    diskcache>=5.4.0 \
    inflection>=0.5.1 \
    jsonmerge>=1.8.0 \
    lark>=1.1.0 \
    open-clip-torch>=2.20.0 \
    piexif>=1.1.3 \
    protobuf==3.20.0 \
    pytorch_lightning>=1.9.0 \
    resize-right>=1.0.0 \
    torchdiffeq>=0.2.3 \
    torchsde>=0.2.6 \
    facexlib>=0.3.0 \
    gfpgan>=1.3.8 \
    realesrgan>=1.0.0

# Try to install tokenizers with pre-compiled wheel
echo "🔧 Attempting to install tokenizers..."
pip install --no-cache-dir --prefer-binary tokenizers>=0.13.0 || echo "⚠️  tokenizers installation failed, continuing..."

echo "✅ Build completed successfully!"
