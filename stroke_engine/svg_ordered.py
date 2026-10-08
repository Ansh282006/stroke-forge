"""Render an ordered DrawableRepresentation to SVG."""
from __future__ import annotations

from pathlib import Path as FsPath

from vectorization.representation import DrawableRepresentation


def _path_d(points, closed):
    if not points:
        return ""
    head = f"M {points[0][0]:.2f} {points[0][1]:.2f}"
    body = " ".join(f"L {x:.2f} {y:.2f}" for x, y in points[1:])
    return f"{head} {body}{' Z' if closed else ''}"


def render_svg_ordered(rep, path: FsPath,
                       stroke_color: str = "#111111",
                       stroke_width: float = 1.5,
                       background: str = "#ffffff",
                       include_order_labels: bool = True) -> None:
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{rep.canvas_width}" height="{rep.canvas_height}" '
        f'viewBox="0 0 {rep.canvas_width} {rep.canvas_height}">',
        f'<rect width="100%" height="100%" fill="{background}"/>',
        f'<g fill="none" stroke="{stroke_color}" '
        f'stroke-width="{stroke_width}" stroke-linecap="round" '
        f'stroke-linejoin="round">',
    ]
    ordered = sorted(rep.paths, key=lambda p: p.order)
    for p in ordered:
        d = _path_d([(pt.x, pt.y) for pt in p.points], p.closed)
        if d:
            lines.append(
                f'  <path id="{p.id}" data-order="{p.order}" '
                f'data-importance="{p.importance:.3f}" d="{d}"/>'
            )
    lines.append("</g>")
    if include_order_labels:
        for p in ordered:
            x, y, w, h = p.bbox
            lines.append(
                f'<text x="{x + w/2:.1f}" y="{y + h/2:.1f}" '
                f'font-family="monospace" font-size="10" fill="#cc0000" '
                f'text-anchor="middle">{p.order}</text>'
            )
    lines.append("</svg>")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
