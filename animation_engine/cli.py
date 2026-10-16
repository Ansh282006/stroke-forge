"""Animation engine CLI (M5)."""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
from .timeline import build_animation_timeline
from .svg_animator import render_animated_svg
from .player import render_player_html

def _slug(s): return "".join(c if c.isalnum() or c in "-_" else "_" for c in s).strip("_") or "out"

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

    in_path = Path(args.input); out_dir = Path(args.output); out_dir.mkdir(parents=True, exist_ok=True)
    doc = json.loads(in_path.read_text(encoding="utf-8"))
    timeline = build_animation_timeline(doc, speed=args.speed, gap_ms=args.gap_ms,
                                        loop=args.loop, loop_delay_ms=args.loop_delay_ms)
    svg = render_animated_svg(doc, timeline, autoplay=not args.no_autoplay)
    base = _slug(args.name or in_path.stem)
    (out_dir / f"{base}_animated.svg").write_text(svg, encoding="utf-8")
    html_out = render_player_html(svg, title=f"StrokeForge - {base}",
                                  autoplay=not args.no_autoplay, loop=args.loop,
                                  loop_delay_ms=args.loop_delay_ms, total_ms=timeline.total_ms)
    (out_dir / f"{base}_player.html").write_text(html_out, encoding="utf-8")
    (out_dir / f"{base}_animation.json").write_text(json.dumps(timeline.to_dict(), indent=2), encoding="utf-8")
    if args.verbose:
        print(f"[M5] entries={len(timeline.entries)} total_ms={timeline.total_ms} name={base}")
    return 0

if __name__ == "__main__":
    sys.exit(main())