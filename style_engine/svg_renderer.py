"""Styled SVG renderer with optional glow (M4)."""
from __future__ import annotations
from typing import List
from .apply import StyledRepresentation

def _d(pts: List[List[float]]) -> str:
    if not pts: return ""
    s = f"M {pts[0][0]:.2f} {pts[0][1]:.2f}"
    for p in pts[1:]:
        s += f" L {p[0]:.2f} {p[1]:.2f}"
    return s

def render(styled: StyledRepresentation) -> str:
    W = styled.canvas.get("width", 512); H = styled.canvas.get("height", 512)
    s = styled.style
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">']
    if s.glow:
        parts.append(
            '<defs>'
            f'<filter id="sf-glow" x="-50%" y="-50%" width="200%" height="200%">'
            f'<feGaussianBlur stdDeviation="{s.glow_radius}" result="blur"/>'
            '<feMerge>'
            '<feMergeNode in="blur"/><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/>'
            '</feMerge></filter></defs>'
        )
    parts.append(f'<rect width="{W}" height="{H}" fill="{s.background}"/>')
    for p in styled.paths:
        glow = ' filter="url(#sf-glow)"' if s.glow else ""
        parts.append(
            f'<path d="{_d(p.points)}" fill="{s.fill}" stroke="{s.stroke_color}" '
            f'stroke-width="{s.stroke_width}" stroke-linecap="{s.linecap}" '
            f'stroke-linejoin="{s.linejoin}" opacity="{s.opacity}"{glow} '
            f'data-order="{p.order}"/>'
        )
    parts.append("</svg>")
    return "".join(parts)

def save(styled, path):
    from pathlib import Path as P
    p = P(path); p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(render(styled), encoding="utf-8")