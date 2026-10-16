"""StrokeForge animation engine CLI (M5)."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .timeline import build_animation_timeline
from .svg_animator import render_animated_svg
from .player import render_player_html


def _slug(s: str) -> str:
    cleaned = "".join(c if c.isalnum() or c in "-_" else "_" for c in s).strip("_")
    return cleaned or "out"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="StrokeForge animation engine (M5)")
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--name", default=None)
    ap.add_argument("--speed", type=float, default=1.0)
    ap.add_argument("--gap-ms", type=int, default=0)
    ap.add_argument("--loop", action="store_true")
    ap.add_argument("--loop-delay-ms", type=int, default=400)
    ap.add_argument("--no-autoplay", action="store_true")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args(argv)

    in_path = Path(args.input)
    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)

    with in_path.open("r", encoding="utf-8") as f:
        doc = json.load(f)

    timeline = build_animation_timeline(
        doc,
        speed=args.speed,
        gap_ms=args.gap_ms,
        loop=args.loop,
        loop_delay_ms=args.loop_delay_ms,
    )

    svg = render_animated_svg(doc, timeline, autoplay=not args.no_autoplay)

    base = _slug(args.name or in_path.stem)

    svg_path = out_dir / f"{base}_animated.svg"
    svg_path.write_text(svg, encoding="utf-8")

    html_out = render_player_html(
        svg,
        title=f"StrokeForge - {base}",
        autoplay=not args.no_autoplay,
        loop=args.loop,
        loop_delay_ms=args.loop_delay_ms,
        total_ms=timeline.total_ms,
    )
    html_path = out_dir / f"{base}_player.html"
    html_path.write_text(html_out, encoding="utf-8")

    anim_path = out_dir / f"{base}_animation.json"
    anim_path.write_text(json.dumps(timeline.to_dict(), indent=2), encoding="utf-8")

    if args.verbose:
        print(f"[M5] input        : {in_path}")
        print(f"[M5] paths        : {len(doc.get('paths', []))}")
        print(f"[M5] entries      : {len(timeline.entries)}")
        print(f"[M5] total_ms     : {timeline.total_ms}")
        print(f"[M5] speed        : {args.speed}")
        print(f"[M5] loop         : {timeline.loop}")
        print(f"[M5] wrote SVG    : {svg_path}")
        print(f"[M5] wrote HTML   : {html_path}")
        print(f"[M5] wrote JSON   : {anim_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
