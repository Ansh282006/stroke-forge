"""Style engine CLI (M4)."""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
from .styles import get_style, list_styles
from .apply import apply_style
from .svg_renderer import save as save_svg

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="StrokeForge style engine (M4)")
    ap.add_argument("--input", required=True)
    ap.add_argument("--style", default="outline", choices=list_styles())
    ap.add_argument("--output", required=True)
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args(argv)

    with open(args.input, "r", encoding="utf-8") as f:
        doc = json.load(f)

    style = get_style(args.style)
    styled = apply_style(doc, style)
    out = Path(args.output); out.mkdir(parents=True, exist_ok=True)
    stem = Path(args.input).stem.replace("_ordered", "")
    svg_p = out / f"{stem}_{style.name}.svg"
    json_p = out / f"{stem}_{style.name}.json"
    save_svg(styled, svg_p)
    json_p.write_text(json.dumps(styled.to_dict(), indent=2), encoding="utf-8")
    if args.verbose:
        print(f"[M4] style      : {style.name}")
        print(f"[M4] wrote      : {svg_p}")
        print(f"[M4] wrote      : {json_p}")
    return 0

if __name__ == "__main__":
    sys.exit(main())