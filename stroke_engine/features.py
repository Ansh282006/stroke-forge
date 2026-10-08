"""Per-path features used by the ordering algorithm."""
from __future__ import annotations

from dataclasses import dataclass

from vectorization.representation import Path


@dataclass
class PathFeatures:
    id: str
    hierarchy: int
    is_hole: bool
    importance: float
    length: float
    area: float
    cx: float
    cy: float
    top: float
    left: float


def extract_features(path: Path) -> PathFeatures:
    x, y, w, h = path.bbox
    return PathFeatures(
        id=path.id, hierarchy=path.hierarchy, is_hole=path.is_hole,
        importance=path.importance, length=path.length, area=path.area,
        cx=x + w / 2.0, cy=y + h / 2.0, top=y, left=x,
    )
