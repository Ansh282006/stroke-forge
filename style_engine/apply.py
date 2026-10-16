"""Apply a StyleDescriptor to a DrawableRepresentation (M4)."""
from __future__ import annotations
import random
from dataclasses import dataclass, field
from typing import Any, Dict, List
from vectorization.representation import DrawableRepresentation, Path
from .style import StyleDescriptor

@dataclass
class StyledRepresentation:
    canvas: Dict[str, int]
    style: StyleDescriptor
    paths: List[Path]
    timeline: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self):
        return {
            "canvas": self.canvas,
            "style": self.style.to_dict(),
            "paths": [p.to_dict() for p in self.paths],
            "timeline": self.timeline,
        }

def _jitter_points(points, amp, rng):
    if amp <= 0: return points
    return [[x + rng.uniform(-amp, amp), y + rng.uniform(-amp, amp)] for x, y in points]

def apply_style(doc_dict: Dict[str, Any], style: StyleDescriptor, seed: int = 1337) -> StyledRepresentation:
    rng = random.Random(seed)
    paths: List[Path] = []
    for raw in doc_dict.get("paths", []):
        p = Path(**{k: raw[k] for k in raw if k in Path.__dataclass_fields__})
        if style.jitter > 0:
            p.points = _jitter_points(p.points, style.jitter, rng)
        paths.append(p)
    return StyledRepresentation(
        canvas=doc_dict.get("canvas", {"width": 512, "height": 512}),
        style=style,
        paths=paths,
        timeline=doc_dict.get("timeline", {}),
    )