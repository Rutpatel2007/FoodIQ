#!/usr/bin/env bash
# FoodIQ Unix/Linux/macOS Production Launcher
set -e

echo "========================================================"
echo "  FoodIQ -- India Consumer Internet Intelligence Engine"
echo "========================================================"

if ! command -v python3 &> /dev/null; then
    echo "[ERROR] python3 is required but was not found."
    exit 1
fi

if [ ! -f "data/foodiq.db" ]; then
    echo "[WARNING] data/foodiq.db not found. Initializing database..."
    python3 -m backend.app.ingestion.runner
fi

echo "Starting FoodIQ Server on http://127.0.0.1:8000..."
exec python3 -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
