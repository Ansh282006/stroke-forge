"""Animated SVG renderer (M5)."""
from __future__ import annotations
from typing import Any, Dict, List
from xml.sax.saxutils import escape
from .timeline import AnimationTimeline, AnimationEntry

DEFAULTS = {
    "background": "#05060a", "stroke_color": "#00f0ff", "stroke_width": 2.2,
    "opacity": 1.0, "linecap": "round", "linejoin": "round", "glow": True,
}

def _fmt_points(points):
    if not points: return ""
    cmds = [f"M {float(points[0][0]):.2f} {float(points[0][1]):.2f}"]
    for pt in points[1:]:
        cmds.append(f"L {float(pt[0]):.2f} {float(pt[1]):.2f}")
    return " ".join(cmds)

def _resolve_style(doc_style, path_style):
    s = dict(DEFAULTS)
    for src in (doc_style, path_style):
        if src:
            for k, v in src.items():
                if v is not None: s[k] = v
    return s

def _polyline_length(points):
    t = 0.0
    for i in range(1, len(points)):
        dx = float(points[i][0]) - float(points[i-1][0])
        dy = float(points[i][1]) - float(points[i-1][1])
        t += (dx*dx + dy*dy) ** 0.5
    return t

_STYLE = (
    "<style>"
    "@keyframes sf-draw{from{stroke-dashoffset:var(--sf-len);}to{stroke-dashoffset:0;}}"
    ".sf-path{stroke-dasharray:var(--sf-len);stroke-dashoffset:var(--sf-len);"
    "animation-name:sf-draw;animation-duration:var(--sf-dur);"
    "animation-timing-function:var(--sf-ease);animation-delay:var(--sf-delay);"
    "animation-fill-mode:forwards;animation-iteration-count:1;animation-play-state:paused;}"
    ".sf-svg.sf-autoplay .sf-path{animation-play-state:running;}"
    "</style>"
)

def render_animated_svg(styled_doc, timeline: AnimationTimeline, width=None, height=None, autoplay=False):
    canvas = styled_doc.get("canvas") or {}
    W = int(width or canvas.get("width", 512)); H = int(height or canvas.get("height", 512))
    doc_style = styled_doc.get("style") or {}
    paths = styled_doc.get("paths") or []
    entries = {e.path_id: e for e in timeline.entries}
    total = timeline.total_ms if timeline.total_ms > 0 else 1
    root_cls = "sf-svg sf-autoplay" if autoplay else "sf-svg"

    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" class="{root_cls}" data-total-ms="{total}">']
    parts.append('<defs><filter id="sf-glow" x="-50%" y="-50%" width="200%" height="200%">'
                 '<feGaussianBlur stdDeviation="3" result="blur"/><feMerge>'
                 '<feMergeNode in="blur"/><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/>'
                 '</feMerge></filter></defs>')
    parts.append(_STYLE)
    bg = doc_style.get("background", DEFAULTS["background"])
    parts.append(f'<rect x="0" y="0" width="{W}" height="{H}" fill="{escape(str(bg))}"/>')

    for p in paths:
        pid = str(p.get("id", "p?"))
        entry = entries.get(pid)
        if entry is None: continue
        st = _resolve_style(doc_style, p.get("style"))
        d = _fmt_points(p.get("points") or [])
        if not d: continue
        length = float(p.get("length") or 0.0) or max(_polyline_length(p.get("points") or []), 1.0)
        dur, delay = max(1, entry.duration_ms), max(0, entry.start_ms)
        inline = (f"--sf-len:{length:.2f};--sf-dur:{dur}ms;"
                  f"--sf-delay:{delay}ms;--sf-ease:{entry.easing}")
        glow = ' filter="url(#sf-glow)"' if st.get("glow") else ""
        parts.append(
            f'<path class="sf-path" d="{d}" fill="none" '
            f'stroke="{escape(str(st.get("stroke_color")))}" '
            f'stroke-width="{st.get("stroke_width")}" '
            f'stroke-linecap="{escape(str(st.get("linecap")))}" '
            f'stroke-linejoin="{escape(str(st.get("linejoin")))}" '
            f'opacity="{st.get("opacity")}"{glow} '
            f'data-order="{entry.order}" data-path-id="{escape(pid)}" style="{inline}"/>'
        )
    parts.append("</svg>")
    return "".join(parts)