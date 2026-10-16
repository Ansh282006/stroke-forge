"""CSS bundle builder (M6)."""
from __future__ import annotations
from typing import Any, Dict

_BODY = """\
/* StrokeForge generated stylesheet (M6) */
:root { --sf-bg: %(bg)s; --sf-fg: #e7e9ee; }
html, body { background: var(--sf-bg); color: var(--sf-fg); margin: 0; padding: 0; }
@keyframes sf-draw { from { stroke-dashoffset: var(--sf-len); } to { stroke-dashoffset: 0; } }
.sf-path {
  stroke-dasharray: var(--sf-len);
  stroke-dashoffset: var(--sf-len);
  animation-name: sf-draw;
  animation-duration: var(--sf-dur);
  animation-timing-function: var(--sf-ease);
  animation-delay: var(--sf-delay);
  animation-fill-mode: forwards;
  animation-iteration-count: 1;
  animation-play-state: paused;
}
.sf-stage svg.sf-svg { display: block; width: 100%%; height: auto; max-height: 78vh; }
.sf-stage { min-height: 320px; }
"""

def build_css(styled_doc: Dict[str, Any]) -> str:
    style = styled_doc.get("style") or {}
    return _BODY % {"bg": str(style.get("background") or "#05060a")}