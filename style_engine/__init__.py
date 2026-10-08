"""StrokeForge style engine package."""
from .style import StyleDescriptor
from .styles import STYLES, get_style
from .apply import apply_style
from .svg_renderer import render_styled_svg

__all__ = [
    "StyleDescriptor",
    "STYLES",
    "get_style",
    "apply_style",
    "render_styled_svg",
]
