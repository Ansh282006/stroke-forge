"""Tailwind config builder (M6)."""
from __future__ import annotations
import json
from typing import Any, Dict

def build_tailwind_config(styled_doc: Dict[str, Any]) -> str:
    style = styled_doc.get("style") or {}
    body = {"theme": {"extend": {"colors": {
        "sf-bg": str(style.get("background") or "#05060a"),
        "sf-accent": str(style.get("stroke_color") or "#00f0ff"),
        "sf-surface": "rgba(255,255,255,0.04)",
    }, "fontFamily": {"sf": ["ui-sans-serif", "system-ui", "sans-serif"]}}}}
    return ("// StrokeForge generated Tailwind config (M6)\ntailwind.config = "
            + json.dumps(body, indent=2) + ";\n")