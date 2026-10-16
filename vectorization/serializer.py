"""JSON save/load (M2)."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Any, Dict
from .representation import Path, DrawableRepresentation

def save(doc: DrawableRepresentation, path) -> Path:
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(doc.to_dict(), indent=2), encoding="utf-8")
    return path

def load(path) -> DrawableRepresentation:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    paths = [Path(**p) for p in data.get("paths", [])]
    return DrawableRepresentation(
        canvas=data.get("canvas", {}),
        source=data.get("source", {}),
        paths=paths,
        metadata=data.get("metadata", {}),
    )