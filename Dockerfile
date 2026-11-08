# FoodIQ Production Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies including Chromium for PDF generation
RUN apt-get update && apt-get install -y --no-install-recommends \
    chromium \
    sqlite3 \
    curl \
    && rm -rf /var/lib/apt/lists/*

ENV CHROME_BIN=/usr/bin/chromium
ENV PYTHONUNBUFFERED=1
ENV FOODIQ_ENV=production

# Install Python requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY backend/ ./backend/
COPY frontend/ ./frontend/
COPY data/ ./data/
COPY docs/ ./docs/
COPY reports/ ./reports/

EXPOSE 8000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health || exit 1

CMD ["python", "-m", "uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
