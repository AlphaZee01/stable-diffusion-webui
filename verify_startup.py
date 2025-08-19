#!/usr/bin/env python3
"""
Startup verification script for Stable Diffusion WebUI API
"""

import os
import sys
from pathlib import Path

def verify_startup():
    """Verify that the API can start properly"""
    
    print("🔍 Verifying startup configuration...")
    
    # Check environment variables
    required_env_vars = ['SD_WEBUI_RESTARTING', 'API_ONLY']
    for var in required_env_vars:
        if os.getenv(var):
            print(f"✅ {var} = {os.getenv(var)}")
        else:
            print(f"⚠️  {var} not set")
    
    # Check port configuration
    port = os.getenv('PORT', '10000')
    print(f"✅ Port configured: {port}")
    
    # Check CORS origins
    origins = os.getenv('ALLOW_ORIGINS', 'https://uwear-virtual-shop.onrender.com,http://localhost:3000,http://localhost:5173')
    print(f"✅ CORS origins: {origins}")
    
    # Check if main.py exists
    if Path('main.py').exists():
        print("✅ main.py found")
    else:
        print("❌ main.py not found")
        return False
    
    # Check if requirements.txt exists
    if Path('requirements.txt').exists():
        print("✅ requirements.txt found")
    else:
        print("❌ requirements.txt not found")
        return False
    
    print("✅ Startup verification completed successfully!")
    return True

if __name__ == "__main__":
    success = verify_startup()
    sys.exit(0 if success else 1)
