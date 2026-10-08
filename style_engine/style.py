"""StyleDescriptor: single, reusable model describing any drawing style.

Every style (Outline, Neon, Sketch, ...) is expressed as a StyleDescriptor.
The renderer, animation engine, and code generator only ever consume this
structure -- they do not know the name of the style.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class StyleDescriptor:
    name: str
    background: str
    stroke_color: str
    stroke_width: float
    opacity: float

    linecap: str = "round"
    linejoin: str = "round"

    glow: bool = False
    glow_color: str = "#ffffff"
    glow_radius: float = 4.0
    glow_opacity: float = 0.9

    flicker: bool = False

    # Reserved for later styles; ignored by Outline/Neon.
    roughness: float = 0.0
    extra: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "StyleDescriptor":
        return cls(**d)
