from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

STORAGE_DIR = PROJECT_ROOT / "storage"

RAW_DIR = STORAGE_DIR / "raw"

PROCESSED_DIR = STORAGE_DIR / "processed"

VECTOR_DB_DIR = STORAGE_DIR / "vectordb"

CONFIG_DIR = PROJECT_ROOT / "config"