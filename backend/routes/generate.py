"""Generate route (M7)."""
from __future__ import annotations
from pathlib import Path
from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from backend.config import get_settings
from backend.schemas import GenerateResponse
from backend.services.pipeline_service import process_image
from backend.services.job_store import JobRecord, JobStore

router = APIRouter()

@router.post("/generate", response_model=GenerateResponse)
async def generate(
    image: UploadFile = File(...),
    style: str = Form("outline"),
    name: str = Form(""),
    loop: bool = Form(True),
    speed: float = Form(1.0),
) -> GenerateResponse:
    settings = get_settings()
    raw = await image.read()
    if len(raw) > settings.max_upload_bytes:
        raise HTTPException(status_code=413, detail="upload too large")
    if not raw:
        raise HTTPException(status_code=400, detail="empty upload")

    try:
        result = process_image(
            raw, image.filename or "input.png", style,
            job_root=settings.uploads_dir,
            name=name or None, loop=loop, speed=speed,
        )
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"unknown style: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"pipeline error: {e}")

    store = JobStore(settings.uploads_dir)
    rec = JobRecord(
        job_id=result.job_id, status="done", style=result.style, name=result.name,
        total_ms=result.total_ms, files=result.files,
        preview_url=f"/api/jobs/{result.job_id}/files/index.html",
        bundle_url=f"/api/jobs/{result.job_id}/bundle",
    )
    store.save(rec)
    return GenerateResponse(**rec.__dict__)