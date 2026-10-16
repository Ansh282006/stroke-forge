"""StrokeForge animation engine (M5).

Consumes the styled/ordered JSON produced by M3/M4 and emits:

  - an animated SVG where each path draws itself using CSS
    ``stroke-dasharray`` / ``stroke-dashoffset`` keyframes
  - a standalone HTML player with play / pause / restart / speed controls
  - an animation JSON description (for the M6 code generator)

Public API:
    build_animation_timeline(doc, ...) -> AnimationTimeline
    render_animated_svg(doc, timeline, ...) -> str
    render_player_html(svg, ...) -> str
"""

from .timeline import (
    AnimationEntry,
    AnimationTimeline,
    EASING_CSS,
    build_animation_timeline,
    normalize_easing,
)
from .svg_animator import render_animated_svg
from .player import render_player_html

__all__ = [
    "AnimationEntry",
    "AnimationTimeline",
    "EASING_CSS",
    "build_animation_timeline",
    "normalize_easing",
    "render_animated_svg",
    "render_player_html",
]
