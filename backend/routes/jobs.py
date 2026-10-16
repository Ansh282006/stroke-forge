"""Jobs routes (M7)."""
from __future__ import annotations
import io, zipfile
from pathlib import Path
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, Response
from backend.config import get_settings
from backend.schemas import JobStatus
from backend.services.job_store import JobStore

router = APIRouter()

@router.get("/jobs/{job_id}", response_model=JobStatus)
def get_job(job_id: str) -> JobStatus:
    store = JobStore(get_settings().uploads_dir)
    rec = store.get(job_id)
    if not rec: raise HTTPException(status_code=404, detail="job not found")
    return JobStatus(**rec.__dict__)

@router.get("/jobs/{job_id}/files/{name}")
def get_file(job_id: str, name: str):
    store = JobStore(get_settings().uploads_dir)
    rec = store.get(job_id)
    if not rec: raise HTTPException(status_code=404, detail="job not found")
    bundle = Path(store.root) / job_id / "web" / rec.name
    target = bundle / name
    if not target.exists() or target.is_dir():
        raise HTTPException(status_code=404, detail="file not found")
    return FileResponse(target)

@router.get("/jobs/{job_id}/bundle")
def get_bundle(job_id: str):
    store = JobStore(get_settings().uploads_dir)
    rec = store.get(job_id)
    if not rec: raise HTTPException(status_code=404, detail="job not found")
    bundle = Path(store.root) / job_id / "web" / rec.name
    if not bundle.exists(): raise HTTPException(status_code=404, detail="bundle not found")
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for f in bundle.rglob("*"):
            if f.is_file():
                z.write(f, f.relative_to(bundle))
    buf.seek(0)
    return Response(content=buf.getvalue(), media_type="application/zip",
                    headers={"Content-Disposition": f'attachment; filename="{rec.name}.zip"'})