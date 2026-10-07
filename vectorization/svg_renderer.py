"""Render a DrawableRepresentation to a plain SVG file (for verification)."""
from __future__ import annotations

from pathlib import Path as FsPath

from .representation import DrawableRepresentation


def _path_d(points: list[tuple[float, float]], closed: bool) -> str:
    if not points:
        return ""
    head = f"M {points[0][0]:.2f} {points[0][1]:.2f}"
    body = " ".join(f"L {x:.2f} {y:.2f}" for x, y in points[1:])
    tail = " Z" if closed else ""
    return f"{head} {body}{tail}"


def render_svg(
    rep: DrawableRepresentation,
    path: FsPath,
    stroke_color: str = "#111111",
    stroke_width: float = 1.5,
    background: str = "#ffffff",
) -> None:
    lines: list[str] = []
    lines.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{rep.canvas_width}" height="{rep.canvas_height}" '
        f'viewBox="0 0 {rep.canvas_width} {rep.canvas_height}">'
    )
    lines.append(f'<rect width="100%" height="100%" fill="{background}"/>')
    lines.append(
        f'<g fill="none" stroke="{stroke_color}" '
        f'stroke-width="{stroke_width}" stroke-linecap="round" '
        f'stroke-linejoin="round">'
    )
    for p in rep.paths:
        d = _path_d([(pt.x, pt.y) for pt in p.points], p.closed)
        if d:
            lines.append(f'  <path id="{p.id}" d="{d}"/>')
    lines.append("</g>")
    lines.append("</svg>")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
