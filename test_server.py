#!/usr/bin/env python3
"""Simple test server to verify basic functionality"""

from fastapi import FastAPI
import uvicorn
import json
import os

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "CSM Streaming Server Running", "status": "ok"}

@app.get("/config")
async def get_config():
    config_path = "config/app_config.json"
    if os.path.exists(config_path):
        with open(config_path) as f:
            return json.load(f)
    return {"error": "No config found"}

@app.get("/health")
async def health():
    checks = {
        "server": "ok",
        "config": os.path.exists("config/app_config.json"),
        "model_path": "/home/incode/cache/checkpoint-33800",
        "model_exists": os.path.exists("/home/incode/cache/checkpoint-33800")
    }
    return checks

if __name__ == "__main__":
    print("Starting test server on http://0.0.0.0:8001")
    print("Config points to model at: /home/incode/cache/checkpoint-33800")
    uvicorn.run(app, host="0.0.0.0", port=8001)