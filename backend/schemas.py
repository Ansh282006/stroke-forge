"""Pydantic v2 schemas (M7)."""
from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, Field

class StyleOption(BaseModel):
    name: str
    label: str

class GenerateResponse(BaseModel):
    job_id: str
    status: str
    style: str
    name: str
    total_ms: int = 0
    files: List[str] = Field(default_factory=list)
    preview_url: str
    bundle_url: str

class JobStatus(BaseModel):
    job_id: str
    status: str
    style: str
    name: str
    total_ms: int = 0
    files: List[str] = Field(default_factory=list)
    preview_url: str
    bundle_url: str
    error: Optional[str] = None

class Health(BaseModel):
    status: str = "ok"
    version: str = "0.7.0"