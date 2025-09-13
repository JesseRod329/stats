#!/bin/bash

echo "🎙️ Wrestling News Hub - Deploying..."
echo "======================================"

# Kill any existing processes
echo "🔄 Stopping existing servers..."
pkill -f "python3.*app.py" 2>/dev/null || true
pkill -f "python3.*http.server" 2>/dev/null || true

# Wait a moment
sleep 2

# Start backend on port 5001
echo "🚀 Starting Flask backend on port 5001..."
cd scripts
TWITTER_BEARER_TOKEN="AAAAAAAAAAAAAAAAAAAAADua4AEAAAAAHwAeVbnjlTagmgGu3y3%2BiBhzwGw%3DwLNcL4hurAfK0ECMc0kmqr0LoCqbkLvkLN4hgtwuMOWFoVnPnd" PORT=5001 python3 app.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 3

# Start frontend on port 8080
echo "🌐 Starting frontend on port 8080..."
cd ..
python3 -m http.server 8080 &
FRONTEND_PID=$!

# Wait a moment
sleep 2

echo ""
echo "✅ Deployment Complete!"
echo "======================"
echo "🌐 Frontend: http://localhost:8080"
echo "🔧 Backend API: http://localhost:5001/api/tweets"
echo "📊 Health Check: http://localhost:5001/api/health"
echo ""
echo "🎙️ Your X posts are now live in the ticker!"
echo ""
echo "Press Ctrl+C to stop both servers"

# Keep script running and handle cleanup
trap 'echo ""; echo "🛑 Stopping servers..."; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit 0' INT

# Wait for processes
wait
