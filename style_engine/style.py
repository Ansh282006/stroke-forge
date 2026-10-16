"""StyleDescriptor dataclass (M4)."""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any, Dict

@dataclass
class StyleDescriptor:
    name: str = "outline"
    background: str = "#05060a"
    stroke_color: str = "#00f0ff"
    stroke_width: float = 2.2
    opacity: float = 1.0
    linecap: str = "round"
    linejoin: str = "round"
    glow: bool = False
    glow_color: str = "#00f0ff"
    glow_radius: float = 5.0
    glow_opacity: float = 0.95
    flicker: bool = False
    fill: str = "none"
    jitter: float = 0.0
    taper: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)