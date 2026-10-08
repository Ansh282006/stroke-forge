"""Built-in styles.

Each entry is a plain StyleDescriptor. New styles can be added here without
touching the renderer, animation engine, or code generator.
"""
from __future__ import annotations

from .style import StyleDescriptor


OUTLINE = StyleDescriptor(
    name="outline",
    background="#ffffff",
    stroke_color="#111111",
    stroke_width=1.6,
    opacity=1.0,
    linecap="round",
    linejoin="round",
    glow=False,
)


NEON = StyleDescriptor(
    name="neon",
    background="#05060a",
    stroke_color="#00f0ff",
    stroke_width=2.2,
    opacity=1.0,
    linecap="round",
    linejoin="round",
    glow=True,
    glow_color="#00f0ff",
    glow_radius=5.0,
    glow_opacity=0.95,
    flicker=True,
)


STYLES: dict[str, StyleDescriptor] = {
    OUTLINE.name: OUTLINE,
    NEON.name: NEON,
}


def get_style(name: str) -> StyleDescriptor:
    key = name.strip().lower()
    if key not in STYLES:
        raise KeyError(
            f"Unknown style '{name}'. Available: {sorted(STYLES.keys())}"
        )
    return STYLES[key]
