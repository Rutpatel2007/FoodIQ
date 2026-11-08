from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from backend.app.database import get_db

router = APIRouter()

@router.get("/health")
def health_check(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {
        "status": "healthy",
        "service": "FoodIQ Competitive Intelligence Engine",
        "version": "3.1.0",
        "database": "connected"
    }

@router.get("/health/ready")
def readiness_check(db: Session = Depends(get_db)):
    """Deep readiness probe verifying database tables, WAL status, and storage."""
    # 1. DB ping
    db.execute(text("SELECT 1"))
    
    # 2. Check key table record counts
    companies_cnt = db.execute(text("SELECT COUNT(*) FROM companies")).scalar() or 0
    docs_cnt = db.execute(text("SELECT COUNT(*) FROM source_documents")).scalar() or 0
    obs_cnt = db.execute(text("SELECT COUNT(*) FROM metric_observations")).scalar() or 0
    rules_cnt = db.execute(text("SELECT COUNT(*) FROM comparability_rules")).scalar() or 0
    
    # 3. Check WAL journal mode
    journal_mode = db.execute(text("PRAGMA journal_mode")).scalar() or "delete"
    
    # 4. Check integrity
    integrity = db.execute(text("PRAGMA integrity_check")).scalar() or "unknown"
    
    is_ready = companies_cnt >= 2 and docs_cnt >= 10 and obs_cnt >= 500 and integrity == "ok"
    
    return {
        "status": "READY" if is_ready else "NOT_READY",
        "database": {
            "connected": True,
            "journal_mode": str(journal_mode).upper(),
            "integrity": integrity,
            "counts": {
                "companies": companies_cnt,
                "source_documents": docs_cnt,
                "metric_observations": obs_cnt,
                "comparability_rules": rules_cnt
            }
        },
        "version": "3.1.0"
    }
