import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

APP_NAME = os.getenv("APP_NAME", "AeroOps")
DATABASE_PATH = os.getenv(
    "DATABASE_PATH",
    str(PROJECT_ROOT / "aeroops.db"),
)
API_ENV = os.getenv("API_ENV", "development")