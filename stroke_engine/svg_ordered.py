"""SVG with data-order + red order labels (M3)."""
from __future__ import annotations
from typing import List
from vectorization.representation import DrawableRepresentation

def _d(pts: List[List[float]]) -> str:
    if not pts: return ""
    s = f"M {pts[0][0]:.2f} {pts[0][1]:.2f}"
    for p in pts[1:]:
        s += f" L {p[0]:.2f} {p[1]:.2f}"
    return s

def render(doc: DrawableRepresentation) -> str:
    W = doc.canvas.get("width", 512); H = doc.canvas.get("height", 512)
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">']
    parts.append(f'<rect width="{W}" height="{H}" fill="#ffffff"/>')
    for p in doc.paths:
        parts.append(f'<path d="{_d(p.points)}" fill="none" stroke="#000000" stroke-width="1.4" data-order="{p.order}"/>')
        cx = p.bbox[0] + p.bbox[2] / 2
        cy = p.bbox[1] + p.bbox[3] / 2
        parts.append(f'<text x="{cx:.1f}" y="{cy:.1f}" font-size="10" fill="#ff0055" text-anchor="middle">{p.order}</text>')
    parts.append("</svg>")
    return "".join(parts)

def save(doc, path):
    from pathlib import Path as P
    p = P(path); p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(render(doc), encoding="utf-8")