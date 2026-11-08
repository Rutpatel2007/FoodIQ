# FoodIQ Phase 9 — Production Deployment Guide

## 1. Deployment Overview

FoodIQ is engineered as a portable, standalone, and containerized financial research system. It requires no external Node.js/npm runtime, no external Redis/Celery queue, and no cloud-vendor locked dependencies.

---

## 2. Local Bare-Metal Execution

### Prerequisites
- Python 3.12+
- Google Chrome or Chromium (optional, required only for PDF report compilation)

### Quick Launch on Windows
```bat
REM 1. Clone or navigate to the repository
cd FoodIQ

REM 2. Install dependencies
pip install -r requirements.txt

REM 3. Launch with one click
run_foodiq.bat
```
The server will start on `http://127.0.0.1:8000/`.

### Quick Launch on Linux / macOS
```bash
# 1. Install dependencies
pip3 install -r requirements.txt

# 2. Grant execution permissions
chmod +x run_foodiq.sh

# 3. Launch
./run_foodiq.sh
```

---

## 3. Containerized Docker Deployment

### Single-Command Startup via Docker Compose
```bash
docker compose up -d --build
```

### Manual Docker Build & Run
```bash
docker build -t foodiq:latest .
docker run -d -p 8000:8000 -v $(pwd)/data:/app/data --name foodiq foodiq:latest
```

The container automatically installs Chromium, mounts persistent SQLite storage at `/app/data`, and exposes health checks at `/api/v1/health`.
