"""StrokeForge animation engine (M5)."""
from .timeline import AnimationEntry, AnimationTimeline, EASING_CSS, build_animation_timeline, normalize_easing
from .svg_animator import render_animated_svg
from .player import render_player_html

__all__ = [
    "AnimationEntry", "AnimationTimeline", "EASING_CSS",
    "build_animation_timeline", "normalize_easing",
    "render_animated_svg", "render_player_html",
]