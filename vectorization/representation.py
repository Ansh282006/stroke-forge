"""Drawable data model (M2)."""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional

@dataclass
class Point:
    x: float
    y: float

    def to_list(self): return [self.x, self.y]

@dataclass
class Path:
    id: str
    points: List[List[float]]
    closed: bool = False
    length: float = 0.0
    area: float = 0.0
    bbox: List[float] = field(default_factory=lambda: [0.0, 0.0, 0.0, 0.0])
    hierarchy: int = 0
    is_hole: bool = False
    parent_id: Optional[str] = None
    importance: float = 0.0
    order: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class DrawableRepresentation:
    canvas: Dict[str, int]
    source: Dict[str, str]
    paths: List[Path] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "canvas": self.canvas,
            "source": self.source,
            "metadata": self.metadata,
            "paths": [p.to_dict() for p in self.paths],
        }