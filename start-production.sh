#!/bin/bash

# Production startup script for Stable Diffusion WebUI API
# This script sets up the environment and starts the API service

echo "🚀 Starting Stable Diffusion WebUI API in Production Mode..."

# Set environment variables
export SD_WEBUI_RESTARTING=1
export API_ONLY=true
export GRADIO_SERVER_NAME=0.0.0.0
export GRADIO_SERVER_PORT=${PORT:-10000}

# Create models directory if it doesn't exist
mkdir -p models

# Check if we're in a container environment
if [ -f /.dockerenv ]; then
    echo "📦 Running in Docker container"
else
    echo "🖥️  Running on host system"
fi

# Display configuration
echo "📋 Configuration:"
echo "   Port: $GRADIO_SERVER_PORT"
echo "   Host: $GRADIO_SERVER_NAME"
echo "   API Only: $API_ONLY"
echo "   CORS Origins: ${ALLOW_ORIGINS:-https://uwear-virtual-shop.onrender.com,http://localhost:3000,http://localhost:5173}"

# Start the application
echo "🎯 Starting API server..."
python main.py
