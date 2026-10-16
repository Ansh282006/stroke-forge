"""Backend settings (M7)."""
from __future__ import annotations
import os
from dataclasses import dataclass
from pathlib import Path

@dataclass
class Settings:
    host: str = os.environ.get("SF_HOST", "127.0.0.1")
    port: int = int(os.environ.get("SF_PORT", "8000"))
    cors_origins: tuple = tuple((os.environ.get("SF_CORS", "http://localhost:5173,http://127.0.0.1:5173")).split(","))
    uploads_dir: Path = Path(os.environ.get("SF_UPLOADS", "data/outputs/jobs"))
    max_upload_bytes: int = int(os.environ.get("SF_MAX_UPLOAD", str(8 * 1024 * 1024)))

def get_settings() -> Settings:
    return Settings()