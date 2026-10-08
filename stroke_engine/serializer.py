"""Save/load ordered representations (paths + timeline)."""
from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path as FsPath
from typing import Any

from vectorization.representation import DrawableRepresentation

from .timeline import TimelineEntry


def save_ordered(rep, timeline, total_ms, path: FsPath) -> None:
    payload: dict[str, Any] = rep.to_dict()
    payload["timeline"] = {"total_ms": total_ms, "entries": [asdict(e) for e in timeline]}
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)


def load_ordered(path: FsPath) -> tuple[DrawableRepresentation, list[TimelineEntry], int]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    rep = DrawableRepresentation.from_dict(data)
    tl = data.get("timeline", {})
    entries = [TimelineEntry(**e) for e in tl.get("entries", [])]
    return rep, entries, int(tl.get("total_ms", 0))
