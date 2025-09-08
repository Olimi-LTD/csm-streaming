#!/usr/bin/env python3
"""
Simplified server startup script for CSM Streaming
Configured to use model from /home/incode/cache/checkpoint-33800
"""

import os
import sys
import json

# Set the model path configuration
CONFIG_PATH = "config/app_config.json"
MODEL_PATH = "/home/incode/cache/checkpoint-33800"

print(f"CSM Streaming Server Starting...")
print(f"Model path configured: {MODEL_PATH}")

# Check if model exists
if os.path.exists(MODEL_PATH):
    print(f"✓ Model directory found at {MODEL_PATH}")
    model_files = os.listdir(MODEL_PATH)[:5]
    print(f"  Contains: {', '.join(model_files)}...")
else:
    print(f"✗ Warning: Model directory not found at {MODEL_PATH}")

# Check configuration
if os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH) as f:
        config = json.load(f)
    print(f"✓ Configuration loaded from {CONFIG_PATH}")
    print(f"  Model path in config: {config.get('model_path', 'not set')}")
else:
    print(f"✗ No configuration file at {CONFIG_PATH}")

print("\nStarting server components...")

try:
    # Import after checks
    from fastapi import FastAPI, Request
    from fastapi.responses import HTMLResponse
    from fastapi.templating import Jinja2Templates
    from fastapi.staticfiles import StaticFiles
    import uvicorn
    
    app = FastAPI()
    templates = Jinja2Templates(directory="templates")
    app.mount("/static", StaticFiles(directory="static"), name="static")
    
    @app.get("/", response_class=HTMLResponse)
    async def root(request: Request):
        return templates.TemplateResponse("index.html", {"request": request})
    
    @app.get("/setup", response_class=HTMLResponse) 
    async def setup_page(request: Request):
        return templates.TemplateResponse("setup.html", {"request": request})
    
    @app.get("/chat", response_class=HTMLResponse)
    async def chat_page(request: Request):
        return templates.TemplateResponse("chat.html", {"request": request})
    
    @app.get("/config")
    async def get_config():
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH) as f:
                return json.load(f)
        return {"error": "No configuration found"}
    
    print(f"Starting FastAPI server on http://0.0.0.0:8002")
    print(f"Access the web interface at: http://localhost:8002")
    uvicorn.run(app, host="0.0.0.0", port=8002)
    
except ImportError as e:
    print(f"Error importing required modules: {e}")
    print("Please ensure all dependencies are installed")
    sys.exit(1)
except Exception as e:
    print(f"Error starting server: {e}")
    sys.exit(1)