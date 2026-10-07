"""Drawable representation data model.

This is the renderer-independent core of StrokeForge. Every downstream
module (ordering, style, animation, codegen) operates on this model.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class Point:
    x: float
    y: float


@dataclass
class Path:
    id: str
    points: list[Point]
    closed: bool
    length: float
    area: float
    bbox: tuple[float, float, float, float]
    hierarchy: int = 0
    is_hole: bool = False
    parent_id: str | None = None
    importance: float = 0.0
    order: int = 0

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["points"] = [[p.x, p.y] for p in self.points]
        return d

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Path":
        return cls(
            id=d["id"],
            points=[Point(x=p[0], y=p[1]) for p in d["points"]],
            closed=d["closed"],
            length=d["length"],
            area=d["area"],
            bbox=tuple(d["bbox"]),
            hierarchy=d.get("hierarchy", 0),
            is_hole=d.get("is_hole", False),
            parent_id=d.get("parent_id"),
            importance=d.get("importance", 0.0),
            order=d.get("order", 0),
        )


@dataclass
class DrawableRepresentation:
    canvas_width: int
    canvas_height: int
    paths: list[Path]
    source_filename: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "canvas": {
                "width": self.canvas_width,
                "height": self.canvas_height,
            },
            "source": {"filename": self.source_filename},
            "metadata": self.metadata,
            "paths": [p.to_dict() for p in self.paths],
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "DrawableRepresentation":
        return cls(
            canvas_width=d["canvas"]["width"],
            canvas_height=d["canvas"]["height"],
            paths=[Path.from_dict(p) for p in d["paths"]],
            source_filename=d.get("source", {}).get("filename", ""),
            metadata=d.get("metadata", {}),
        )
