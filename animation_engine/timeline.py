"""Animation timeline construction (M5).

The M3 stroke engine already attaches a timeline to the drawable
document (start_ms / duration_ms / end_ms / easing per path).  M5
turns that into an animation-specific timeline:

  - normalizes easing names ("easeInOut" -> "ease-in-out") so the SVG
    renderer can drop them straight into CSS
  - optionally inserts a fixed gap between consecutive strokes so the
    drawing reads stroke-by-stroke instead of as a continuous line
  - scales every duration by a global ``speed`` factor so the player
    can slow / speed the whole animation without touching the SVG
  - preserves the original order so replay is deterministic

The output is a plain dataclass, fully serializable to JSON.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


EASING_CSS: Dict[str, str] = {
    "linear": "linear",
    "ease": "ease",
    "easein": "ease-in",
    "easeout": "ease-out",
    "easeinout": "ease-in-out",
    "ease_in": "ease-in",
    "ease_out": "ease-out",
    "ease_in_out": "ease-in-out",
    "easeIn": "ease-in",
    "easeOut": "ease-out",
    "easeInOut": "ease-in-out",
}


def normalize_easing(name: Optional[str]) -> str:
    """Map any easing spelling the pipeline may produce to a CSS keyword."""
    if not name:
        return "ease-in-out"
    if name in EASING_CSS:
        return EASING_CSS[name]
    key = name.replace("-", "").replace("_", "").lower()
    return EASING_CSS.get(key, "ease-in-out")


@dataclass
class AnimationEntry:
    """One animated stroke, in milliseconds."""
    path_id: str
    order: int
    start_ms: int
    duration_ms: int
    end_ms: int
    easing: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "path_id": self.path_id,
            "order": self.order,
            "start_ms": self.start_ms,
            "duration_ms": self.duration_ms,
            "end_ms": self.end_ms,
            "easing": self.easing,
        }


@dataclass
class AnimationTimeline:
    """Ordered animation schedule for the whole drawing."""
    total_ms: int
    entries: List[AnimationEntry] = field(default_factory=list)
    loop: bool = False
    loop_delay_ms: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_ms": self.total_ms,
            "loop": self.loop,
            "loop_delay_ms": self.loop_delay_ms,
            "entries": [e.to_dict() for e in self.entries],
        }


def _fallback_entries_from_paths(doc: Dict[str, Any]) -> List[Dict[str, Any]]:
    entries: List[Dict[str, Any]] = []
    cursor = 0
    for p in doc.get("paths", []):
        dur = max(120, int(float(p.get("length", 100.0)) * 3))
        entries.append(
            {
                "path_id": p.get("id", "p?"),
                "order": p.get("order", 0),
                "start_ms": cursor,
                "duration_ms": dur,
                "end_ms": cursor + dur,
                "easing": "easeInOut",
            }
        )
        cursor += dur
    return entries


def build_animation_timeline(
    ordered_doc: Dict[str, Any],
    speed: float = 1.0,
    gap_ms: int = 0,
    loop: bool = False,
    loop_delay_ms: int = 0,
) -> AnimationTimeline:
    """Build an AnimationTimeline from an ordered/styled document."""
    if speed <= 0:
        raise ValueError("speed must be > 0")

    src = ordered_doc.get("timeline") or {}
    src_entries = list(src.get("entries") or [])
    if not src_entries:
        src_entries = _fallback_entries_from_paths(ordered_doc)

    entries: List[AnimationEntry] = []
    cursor = 0
    for raw in sorted(src_entries, key=lambda e: e.get("order", 0)):
        dur = max(1, int(round(float(raw.get("duration_ms", 300)) / speed)))
        start = cursor
        end = start + dur
        entries.append(
            AnimationEntry(
                path_id=str(raw.get("path_id", "p?")),
                order=int(raw.get("order", 0)),
                start_ms=start,
                duration_ms=dur,
                end_ms=end,
                easing=normalize_easing(raw.get("easing")),
            )
        )
        cursor = end + int(gap_ms)

    total = cursor - int(gap_ms) if entries else 0
    total = max(total, 0)

    return AnimationTimeline(
        total_ms=total,
        entries=entries,
        loop=bool(loop),
        loop_delay_ms=int(loop_delay_ms),
    )
