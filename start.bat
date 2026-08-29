@echo off
title AegisAI — Autonomous Cyber Defense Command Center
echo ========================================================
echo   AegisAI - Autonomous Adaptive Cyber Defense Agent
echo   Smart India Hackathon 2026 Edition
echo ========================================================
echo.

echo [1/3] Checking Python Dependencies...
python -m pip install -r backend/requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Failed to install Python dependencies.
    pause
    exit /b 1
)

echo.
echo [2/3] Starting AegisAI Backend Server (FastAPI + WebSocket)...
start "AegisAI Backend [Port 8000]" cmd /k "python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload"

echo.
echo [3/3] Starting AegisAI SOC Frontend Dashboard (Vite)...
cd frontend
start "AegisAI SOC Dashboard [Port 5173]" cmd /k "npm run dev"
cd ..

echo.
echo ========================================================
echo   AegisAI Services are now starting!
echo   - Backend API & WebSocket: http://localhost:8000
echo   - Interactive SOC Dashboard: http://localhost:5173
echo   - API Docs (Swagger): http://localhost:8000/docs
echo ========================================================
echo.
echo Press any key to open the dashboard in your default browser...
pause >nul
start http://localhost:5173
