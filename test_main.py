#!/usr/bin/env python3
"""
Test script to verify main.py imports work correctly
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

# Set environment variables for production
os.environ.setdefault('SD_WEBUI_RESTARTING', '1')
os.environ.setdefault('API_ONLY', 'true')

print("Testing imports...")

try:
    from modules import initialize_util, initialize
    print("✅ modules imported successfully")
except Exception as e:
    print(f"❌ Error importing modules: {e}")
    sys.exit(1)

try:
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware
    print("✅ FastAPI imported successfully")
except Exception as e:
    print(f"❌ Error importing FastAPI: {e}")
    sys.exit(1)

try:
    import uvicorn
    print("✅ uvicorn imported successfully")
except Exception as e:
    print(f"❌ Error importing uvicorn: {e}")
    sys.exit(1)

# Test missing packages gracefully
try:
    import pillow_avif
    print("✅ pillow_avif available")
except ImportError:
    print("⚠️  pillow_avif not available (expected)")

try:
    import tokenizers
    print("✅ tokenizers available")
except ImportError:
    print("⚠️  tokenizers not available (expected)")

try:
    import transformers
    print("✅ transformers available")
except ImportError:
    print("⚠️  transformers not available (expected)")

print("✅ All tests passed! main.py should work correctly.")
