# FoodIQ Configuration
import os
from pathlib import Path
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseModel):
    PROJECT_NAME: str = "FoodIQ Competitive Intelligence Engine"
    API_V1_PREFIX: str = "/api/v1"
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'data' / 'foodiq.db'}")
    BASE_DIR: Path = BASE_DIR
    DATA_DIR: Path = BASE_DIR / "data"
    REPORTS_DIR: Path = BASE_DIR / "data" / "reports"
    SWIGGY_PACK_DIR: Path = BASE_DIR / "FoodIQ_Swiggy_Compact"
    ETERNAL_PACK_DIR: Path = BASE_DIR / "FoodIQ_Eternal_Compact"

settings = Settings()

# Ensure required directories exist
os.makedirs(settings.DATA_DIR, exist_ok=True)
os.makedirs(settings.REPORTS_DIR, exist_ok=True)
