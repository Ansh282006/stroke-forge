"""Plain SVG renderer (M2)."""
from __future__ import annotations
from typing import List
from .representation import DrawableRepresentation, Path

def _d(points: List[List[float]]) -> str:
    if not points: return ""
    s = f"M {points[0][0]:.2f} {points[0][1]:.2f}"
    for p in points[1:]:
        s += f" L {p[0]:.2f} {p[1]:.2f}"
    return s

def render(doc: DrawableRepresentation) -> str:
    W = doc.canvas.get("width", 512); H = doc.canvas.get("height", 512)
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">']
    parts.append(f'<rect width="{W}" height="{H}" fill="#ffffff"/>')
    for p in doc.paths:
        parts.append(f'<path d="{_d(p.points)}" fill="none" stroke="#000000" stroke-width="1.4"/>')
    parts.append("</svg>")
    return "".join(parts)

def save(doc: DrawableRepresentation, path) -> str:
    from pathlib import Path as P
    svg = render(doc)
    p = P(path); p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(svg, encoding="utf-8")
    return svg