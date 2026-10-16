"""Per-path features (M3)."""
from __future__ import annotations
from typing import Any, Dict
from vectorization.representation import Path

def features(p: Path) -> Dict[str, Any]:
    cx = p.bbox[0] + p.bbox[2] / 2
    cy = p.bbox[1] + p.bbox[3] / 2
    return {
        "id": p.id,
        "length": p.length,
        "area": p.area,
        "bbox": p.bbox,
        "centroid": [cx, cy],
        "closed": p.closed,
        "importance": p.importance,
        "hierarchy": p.hierarchy,
    }