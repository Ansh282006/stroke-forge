"""Animated SVG renderer (M5)."""

from __future__ import annotations

from typing import Any, Dict, List
from xml.sax.saxutils import escape

from .timeline import AnimationTimeline, AnimationEntry


DEFAULTS: Dict[str, Any] = {
    "background": "#05060a",
    "stroke_color": "#00f0ff",
    "stroke_width": 2.2,
    "opacity": 1.0,
    "linecap": "round",
    "linejoin": "round",
    "glow": True,
}


def _fmt_points(points: List[List[float]]) -> str:
    if not points:
        return ""
    cmds = [f"M {float(points[0][0]):.2f} {float(points[0][1]):.2f}"]
    for pt in points[1:]:
        cmds.append(f"L {float(pt[0]):.2f} {float(pt[1]):.2f}")
    return " ".join(cmds)


def _resolve_style(doc_style, path_style) -> Dict[str, Any]:
    s = dict(DEFAULTS)
    if doc_style:
        for k, v in doc_style.items():
            if v is not None:
                s[k] = v
    if path_style:
        for k, v in path_style.items():
            if v is not None:
                s[k] = v
    return s


def _entry_by_id(timeline: AnimationTimeline) -> Dict[str, AnimationEntry]:
    return {e.path_id: e for e in timeline.entries}


def _polyline_length(points) -> float:
    total = 0.0
    for i in range(1, len(points)):
        dx = float(points[i][0]) - float(points[i - 1][0])
        dy = float(points[i][1]) - float(points[i - 1][1])
        total += (dx * dx + dy * dy) ** 0.5
    return total


_STYLE_BLOCK = (
    "<style>"
    "@keyframes sf-draw{"
    "from{stroke-dashoffset:var(--sf-len);}"
    "to{stroke-dashoffset:0;}"
    "}"
    ".sf-path{"
    "stroke-dasharray:var(--sf-len);"
    "stroke-dashoffset:var(--sf-len);"
    "animation-name:sf-draw;"
    "animation-duration:var(--sf-dur);"
    "animation-timing-function:var(--sf-ease);"
    "animation-delay:var(--sf-delay);"
    "animation-fill-mode:forwards;"
    "animation-iteration-count:1;"
    "animation-play-state:paused;"
    "}"
    ".sf-svg.sf-autoplay .sf-path{animation-play-state:running;}"
    "</style>"
)


def render_animated_svg(
    styled_doc: Dict[str, Any],
    timeline: AnimationTimeline,
    width: int | None = None,
    height: int | None = None,
    autoplay: bool = False,
) -> str:
    canvas = styled_doc.get("canvas") or {}
    W = int(width or canvas.get("width", 512))
    H = int(height or canvas.get("height", 512))

    doc_style = styled_doc.get("style") or {}
    paths = styled_doc.get("paths") or []
    entries = _entry_by_id(timeline)
    total_ms = timeline.total_ms if timeline.total_ms > 0 else 1

    root_cls = "sf-svg sf-autoplay" if autoplay else "sf-svg"

    parts: List[str] = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {W} {H}" width="{W}" height="{H}" '
        f'class="{root_cls}" data-total-ms="{total_ms}">'
    )
    parts.append(
        '<defs>'
        '<filter id="sf-glow" x="-50%" y="-50%" width="200%" height="200%">'
        '<feGaussianBlur stdDeviation="3" result="blur"/>'
        '<feMerge>'
        '<feMergeNode in="blur"/>'
        '<feMergeNode in="blur"/>'
        '<feMergeNode in="SourceGraphic"/>'
        '</feMerge>'
        '</filter>'
        '</defs>'
    )
    parts.append(_STYLE_BLOCK)

    bg = doc_style.get("background", DEFAULTS["background"])
    parts.append(
        f'<rect x="0" y="0" width="{W}" height="{H}" fill="{escape(str(bg))}"/>'
    )

    for p in paths:
        pid = str(p.get("id", "p?"))
        entry = entries.get(pid)
        if entry is None:
            continue

        style = _resolve_style(doc_style, p.get("style"))
        points = p.get("points") or []
        d = _fmt_points(points)
        if not d:
            continue

        length = float(p.get("length") or 0.0)
        if length <= 0.0:
            length = max(_polyline_length(points), 1.0)

        dur = max(1, entry.duration_ms)
        delay = max(0, entry.start_ms)
        ease = entry.easing

        stroke = str(style.get("stroke_color", DEFAULTS["stroke_color"]))
        sw = style.get("stroke_width", DEFAULTS["stroke_width"])
        op = style.get("opacity", DEFAULTS["opacity"])
        lc = style.get("linecap", DEFAULTS["linecap"])
        lj = style.get("linejoin", DEFAULTS["linejoin"])
        glow = bool(style.get("glow"))
        glow_filter = ' filter="url(#sf-glow)"' if glow else ""

        inline = (
            f"--sf-len:{length:.2f};"
            f"--sf-dur:{dur}ms;"
            f"--sf-delay:{delay}ms;"
            f"--sf-ease:{ease}"
        )

        parts.append(
            f'<path class="sf-path" d="{d}" fill="none" '
            f'stroke="{escape(stroke)}" stroke-width="{sw}" '
            f'stroke-linecap="{escape(str(lc))}" '
            f'stroke-linejoin="{escape(str(lj))}" '
            f'opacity="{op}"{glow_filter} '
            f'data-order="{entry.order}" data-path-id="{escape(pid)}" '
            f'style="{inline}"/>'
        )

    parts.append("</svg>")
    return "".join(parts)
