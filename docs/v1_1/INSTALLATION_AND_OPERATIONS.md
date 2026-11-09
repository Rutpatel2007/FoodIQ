# FoodIQ v1.1 — Installation, Operations & Deployment Guide
**Document Reference:** DOC-V11-13  
**Classification:** DevOps & Systems Administration  

---

## 1. Quick Start Installation

### Prerequisites
- Python 3.10 or higher.
- Git.

### Step 1: Clone Repository & Virtual Environment
```bash
git clone https://github.com/rutpatel/FoodIQ.git
cd FoodIQ
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
```

### Step 2: Install Dependencies
```bash
pip install -r backend/requirements.txt
```

### Step 3: Start FoodIQ Application
```bash
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```
Open your browser and navigate to: **`http://127.0.0.1:8000`**
