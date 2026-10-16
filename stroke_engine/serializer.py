"""Ordered JSON with timeline (M3)."""
from __future__ import annotations
import json
from pathlib import Path
from vectorization.representation import DrawableRepresentation
from .timeline import build_timeline

def save_ordered(doc: DrawableRepresentation, path) -> Path:
    payload = doc.to_dict()
    payload["timeline"] = build_timeline(doc)
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path