#!/usr/bin/env bash
set -e

echo "========================================================"
echo "  AegisAI - Autonomous Adaptive Cyber Defense Agent"
echo "  Smart India Hackathon 2026 Edition"
echo "========================================================"
echo ""

echo "[1/3] Installing Backend Dependencies..."
python3 -m pip install -r backend/requirements.txt

echo ""
echo "[2/3] Starting Backend Server (FastAPI + WebSocket on Port 8000)..."
python3 -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload &
BACKEND_PID=$!

echo ""
echo "[3/3] Starting Frontend SOC Dashboard (Port 5173)..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "========================================================"
echo "  AegisAI Services are now active!"
echo "  - Backend API: http://localhost:8000"
echo "  - SOC Dashboard: http://localhost:5173"
echo "  - API Swagger Docs: http://localhost:8000/docs"
echo "========================================================"
echo ""

trap "kill $BACKEND_PID $FRONTEND_PID" EXIT
wait
