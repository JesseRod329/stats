#!/usr/bin/env python3
"""
Startup script for Wrestling News Hub
Starts both the Flask backend and serves the frontend
"""

import subprocess
import sys
import os
import time
import threading
import webbrowser
from pathlib import Path

def start_flask_server():
    """Start the Flask backend server"""
    print("🚀 Starting Flask backend server...")
    os.chdir(Path(__file__).parent)
    subprocess.run([sys.executable, 'app.py'])

def start_frontend_server():
    """Start a simple HTTP server for the frontend"""
    print("🌐 Starting frontend server...")
    os.chdir(Path(__file__).parent.parent)  # Go to project root
    
    # Try Python 3's built-in server first
    try:
        subprocess.run([sys.executable, '-m', 'http.server', '8080'])
    except KeyboardInterrupt:
        print("\n👋 Shutting down servers...")

def main():
    """Main startup function"""
    print("🎙️ Wrestling News Hub - Starting up...")
    print("=" * 50)
    
    # Check if requirements are installed
    try:
        import flask
        import flask_cors
        print("✅ Flask dependencies found")
    except ImportError:
        print("❌ Flask dependencies not found. Installing...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
    
    # Start Flask server in a separate thread
    flask_thread = threading.Thread(target=start_flask_server, daemon=True)
    flask_thread.start()
    
    # Wait a moment for Flask to start
    time.sleep(2)
    
    # Start frontend server (this will block)
    try:
        start_frontend_server()
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")

if __name__ == '__main__':
    main()
