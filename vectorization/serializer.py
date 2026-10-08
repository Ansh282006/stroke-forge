"""JSON save/load for the DrawableRepresentation."""
from __future__ import annotations

import json
from pathlib import Path as FsPath

from .representation import DrawableRepresentation


def save_json(rep: DrawableRepresentation, path: FsPath) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(rep.to_dict(), f, indent=2)


def load_json(path: FsPath) -> DrawableRepresentation:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return DrawableRepresentation.from_dict(data)
