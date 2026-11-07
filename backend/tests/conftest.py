import os
import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR))

from backend.app.database import Base, get_db
from backend.app.main import app
from backend.app.config import settings
from backend.app.ingestion.runner import run_full_ingestion

@pytest.fixture(scope="session")
def test_db_session():
    """Provides a database session with full ingested data."""
    # Run ingestion on the database to ensure populated data
    run_full_ingestion()
    from backend.app.database import SessionLocal
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="session")
def client():
    """Provides a FastAPI TestClient."""
    return TestClient(app)
