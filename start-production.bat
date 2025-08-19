@echo off
REM Production startup script for Stable Diffusion WebUI API
REM This script sets up the environment and starts the API service

echo 🚀 Starting Stable Diffusion WebUI API in Production Mode...

REM Set environment variables
set SD_WEBUI_RESTARTING=1
set API_ONLY=true
set GRADIO_SERVER_NAME=0.0.0.0
set GRADIO_SERVER_PORT=%PORT%
if "%GRADIO_SERVER_PORT%"=="" set GRADIO_SERVER_PORT=10000

REM Create models directory if it doesn't exist
if not exist "models" mkdir models

REM Display configuration
echo 📋 Configuration:
echo    Port: %GRADIO_SERVER_PORT%
echo    Host: %GRADIO_SERVER_NAME%
echo    API Only: %API_ONLY%
echo    CORS Origins: %ALLOW_ORIGINS%

REM Start the application
echo 🎯 Starting API server...
python main.py

pause
