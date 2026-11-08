@echo off
REM FoodIQ Windows Production Launcher
echo ========================================================
echo   FoodIQ -- India Consumer Internet Intelligence Engine
echo ========================================================
echo Checking Python environment...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python 3.12+ is required but was not found on PATH.
    pause
    exit /b 1
)

echo Verifying database existence...
if not exist "data\foodiq.db" (
    echo [WARNING] data\foodiq.db not found. Running database initialization...
    python -m backend.app.ingestion.runner
)

echo Starting FoodIQ Server on http://127.0.0.1:8000...
echo Press CTRL+C to terminate.
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
