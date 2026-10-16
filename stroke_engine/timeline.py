"""Duration-proportional timeline (M3)."""
from __future__ import annotations
from typing import Any, Dict
from vectorization.representation import DrawableRepresentation

MIN_MS = 120
MAX_MS = 1200
MS_PER_UNIT = 3.0

def build_timeline(doc: DrawableRepresentation) -> Dict[str, Any]:
    entries = []
    cursor = 0
    for p in doc.paths:
        d = int(max(MIN_MS, min(MAX_MS, p.length * MS_PER_UNIT)))
        entries.append({
            "path_id": p.id,
            "order": p.order,
            "start_ms": cursor,
            "duration_ms": d,
            "end_ms": cursor + d,
            "easing": "easeInOut",
        })
        cursor += d
    return {"total_ms": cursor, "entries": entries}