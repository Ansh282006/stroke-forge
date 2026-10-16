"""Animation timeline (M5)."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

EASING_CSS = {
    "linear": "linear", "ease": "ease",
    "easein": "ease-in", "easeout": "ease-out", "easeinout": "ease-in-out",
    "ease_in": "ease-in", "ease_out": "ease-out", "ease_in_out": "ease-in-out",
    "easeIn": "ease-in", "easeOut": "ease-out", "easeInOut": "ease-in-out",
}

def normalize_easing(name: Optional[str]) -> str:
    if not name: return "ease-in-out"
    if name in EASING_CSS: return EASING_CSS[name]
    key = name.replace("-", "").replace("_", "").lower()
    return EASING_CSS.get(key, "ease-in-out")

@dataclass
class AnimationEntry:
    path_id: str
    order: int
    start_ms: int
    duration_ms: int
    end_ms: int
    easing: str

    def to_dict(self):
        return self.__dict__.copy()

@dataclass
class AnimationTimeline:
    total_ms: int
    entries: List[AnimationEntry] = field(default_factory=list)
    loop: bool = False
    loop_delay_ms: int = 0

    def to_dict(self):
        return {
            "total_ms": self.total_ms, "loop": self.loop,
            "loop_delay_ms": self.loop_delay_ms,
            "entries": [e.to_dict() for e in self.entries],
        }

def _fallback(doc):
    out, cursor = [], 0
    for p in doc.get("paths", []):
        d = max(120, int(float(p.get("length", 100.0)) * 3))
        out.append({"path_id": p.get("id"), "order": p.get("order", 0),
                    "start_ms": cursor, "duration_ms": d, "end_ms": cursor + d,
                    "easing": "easeInOut"})
        cursor += d
    return out

def build_animation_timeline(ordered_doc, speed=1.0, gap_ms=0, loop=False, loop_delay_ms=0):
    if speed <= 0: raise ValueError("speed must be > 0")
    src = (ordered_doc.get("timeline") or {}).get("entries") or []
    if not src: src = _fallback(ordered_doc)
    entries, cursor = [], 0
    for raw in sorted(src, key=lambda e: e.get("order", 0)):
        d = max(1, int(round(float(raw.get("duration_ms", 300)) / speed)))
        entries.append(AnimationEntry(
            path_id=str(raw.get("path_id", "p?")),
            order=int(raw.get("order", 0)),
            start_ms=cursor, duration_ms=d, end_ms=cursor + d,
            easing=normalize_easing(raw.get("easing")),
        ))
        cursor += d + int(gap_ms)
    total = cursor - int(gap_ms) if entries else 0
    return AnimationTimeline(total_ms=max(0, total), entries=entries, loop=bool(loop), loop_delay_ms=int(loop_delay_ms))