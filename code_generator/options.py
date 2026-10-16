"""Generator options (M6)."""
from __future__ import annotations
from dataclasses import asdict, dataclass
from typing import Any, Dict

@dataclass
class GeneratorOptions:
    name: str = "stroke_forge"
    title: str = "StrokeForge"
    autoplay: bool = True
    loop: bool = False
    loop_delay_ms: int = 400
    speed: float = 1.0
    gap_ms: int = 0
    tailwind_cdn: bool = True
    include_readme: bool = True
    include_animation_json: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)