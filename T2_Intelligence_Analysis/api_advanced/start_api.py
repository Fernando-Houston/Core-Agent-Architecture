#!/usr/bin/env python3
"""
Houston Intelligence Platform - Startup Script
Sets up proper paths and starts the integrated API
"""

import sys
import os
from pathlib import Path

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

# Import and run the integrated API
from integrated_api import app
import uvicorn

if __name__ == "__main__":
    print("Starting Houston Intelligence Platform - Integrated API...")
    print("Access points:")
    print("  - API Documentation: http://localhost:8000/docs")
    print("  - WebSocket: ws://localhost:8000/ws")
    print("  - GraphQL Playground: http://localhost:8000/graphql")
    print("  - Demo WebSocket Client: http://localhost:8000/demo")
    print("\nPress Ctrl+C to stop the server\n")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )