# FoodIQ — Development, Testing & Operations Guide

## 1. Local Environment Setup

### Prerequisites
- Python 3.10+ (tested on Python 3.11 and 3.12)
- Git
- SQLite 3.35+

### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone https://github.com/rutpatel/FoodIQ.git
   cd FoodIQ
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Linux/macOS:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Verify environment configuration:**
   Copy `.env.example` to `.env` if custom paths or secrets are required:
   ```bash
   cp .env.example .env
   ```

---

## 2. Running the Application

### Option A: Direct Uvicorn Execution
```bash
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```

### Option B: Convenience Scripts
- **Windows:** Run `run_foodiq.bat`
- **Linux/macOS:** Run `./run_foodiq.sh`

### Option C: Docker Container
```bash
docker compose up --build
```

Access the application in your web browser:
- **Research Workstation UI:** [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **API Documentation (Swagger):** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **API Documentation (ReDoc):** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 3. Running Tests

The test suite includes 145 unit, integration, and regression tests located in `backend/tests/`.

```bash
pytest backend/tests/ -v
```

### Running Specific Test Modules:
- **Analytics & Margin Bridges:** `pytest backend/tests/test_analytics_engines.py`
- **API Endpoints:** `pytest backend/tests/test_api_endpoints.py`
- **Econometrics & Studies:** `pytest backend/tests/test_phase5_quantitative_engine.py`
- **Credibility Engine:** `pytest backend/tests/test_phase4_credibility_engine.py`
- **Lineage & Coordinate Grounding:** `pytest backend/tests/test_lineage_and_provenance.py`
- **Security & Path Traversal:** `pytest backend/tests/test_phase9_production_engineering.py`

---

## 4. Database Operations & Backups

### Creating a Verified Database Backup:
```bash
python scripts/backup_db.py
```
Backups are timestamped and verified with `PRAGMA integrity_check;`.

### Restoring from Backup:
```bash
python scripts/restore_db.py <path_to_backup.db>
```

---

## 5. End-to-End Workflow Verification

Run the integration verification script to test live API health, company records, credibility scores, and econometrics:
```bash
python scripts/verify_v1_1_workflows.py
```
