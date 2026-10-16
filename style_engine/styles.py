"""Built-in styles (M4 + M12)."""
from __future__ import annotations
from typing import Dict
from .style import StyleDescriptor

def outline() -> StyleDescriptor:
    return StyleDescriptor(
        name="outline", background="#ffffff", stroke_color="#111111",
        stroke_width=1.6, glow=False,
    )

def neon() -> StyleDescriptor:
    return StyleDescriptor(
        name="neon", background="#05060a", stroke_color="#00f0ff",
        stroke_width=2.2, glow=True, glow_color="#00f0ff",
        glow_radius=5.0, glow_opacity=0.95, flicker=True,
    )

def sketch() -> StyleDescriptor:
    return StyleDescriptor(
        name="sketch", background="#f7f3ea", stroke_color="#2b2b2b",
        stroke_width=1.4, glow=False, jitter=1.6, taper=True,
    )

def pencil() -> StyleDescriptor:
    return StyleDescriptor(
        name="pencil", background="#fafafa", stroke_color="#3a3a3a",
        stroke_width=1.1, opacity=0.92, glow=False, jitter=0.9, taper=True,
    )

def lineart() -> StyleDescriptor:
    return StyleDescriptor(
        name="lineart", background="#ffffff", stroke_color="#000000",
        stroke_width=1.0, glow=False,
    )

def blueprint() -> StyleDescriptor:
    return StyleDescriptor(
        name="blueprint", background="#0b2447", stroke_color="#a5d8ff",
        stroke_width=1.2, glow=True, glow_color="#a5d8ff", glow_radius=2.4,
    )

def particle() -> StyleDescriptor:
    return StyleDescriptor(
        name="particle", background="#000000", stroke_color="#ff5c00",
        stroke_width=2.4, glow=True, glow_color="#ff9f1c", glow_radius=6.0,
    )

_REGISTRY: Dict[str, callable] = {
    "outline": outline, "neon": neon, "sketch": sketch,
    "pencil": pencil, "lineart": lineart, "blueprint": blueprint,
    "particle": particle,
}

def get_style(name: str) -> StyleDescriptor:
    key = (name or "outline").lower()
    if key not in _REGISTRY:
        raise KeyError(f"unknown style: {name}")
    return _REGISTRY[key]()

def list_styles():
    return sorted(_REGISTRY.keys())