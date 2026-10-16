"""Filesystem job store (M7)."""
from __future__ import annotations
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

@dataclass
class JobRecord:
    job_id: str
    status: str
    style: str
    name: str
    total_ms: int = 0
    files: List[str] = field(default_factory=list)
    preview_url: str = ""
    bundle_url: str = ""
    error: Optional[str] = None

class JobStore:
    def __init__(self, root: Path):
        self.root = Path(root); self.root.mkdir(parents=True, exist_ok=True)

    def _path(self, job_id: str) -> Path:
        return self.root / job_id / "job.json"

    def save(self, record: JobRecord) -> None:
        p = self._path(record.job_id)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(asdict(record), indent=2), encoding="utf-8")

    def get(self, job_id: str) -> Optional[JobRecord]:
        p = self._path(job_id)
        if not p.exists(): return None
        data = json.loads(p.read_text(encoding="utf-8"))
        return JobRecord(**data)

    def list(self) -> List[JobRecord]:
        out: List[JobRecord] = []
        for child in sorted(self.root.iterdir()):
            if child.is_dir():
                rec = self.get(child.name)
                if rec: out.append(rec)
        return out