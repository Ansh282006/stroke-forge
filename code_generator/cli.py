"""Code generator CLI (M6)."""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path
from .options import GeneratorOptions
from .generator import generate_bundle

def _slug(s): return "".join(c if c.isalnum() or c in "-_" else "_" for c in s).strip("_") or "bundle"

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="StrokeForge code generator (M6)")
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--name", default=None)
    ap.add_argument("--title", default=None)
    ap.add_argument("--speed", type=float, default=1.0)
    ap.add_argument("--gap-ms", type=int, default=0)
    ap.add_argument("--loop", action="store_true")
    ap.add_argument("--loop-delay-ms", type=int, default=400)
    ap.add_argument("--no-autoplay", action="store_true")
    ap.add_argument("--no-tailwind-cdn", action="store_true")
    ap.add_argument("--no-readme", action="store_true")
    ap.add_argument("--no-animation-json", action="store_true")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args(argv)

    in_path = Path(args.input); out_dir = Path(args.output); out_dir.mkdir(parents=True, exist_ok=True)
    doc = json.loads(in_path.read_text(encoding="utf-8"))
    name = _slug(args.name or in_path.stem)
    title = args.title or f"StrokeForge - {name}"
    opts = GeneratorOptions(name=name, title=title, autoplay=not args.no_autoplay,
                            loop=args.loop, loop_delay_ms=args.loop_delay_ms,
                            speed=args.speed, gap_ms=args.gap_ms,
                            tailwind_cdn=not args.no_tailwind_cdn,
                            include_readme=not args.no_readme,
                            include_animation_json=not args.no_animation_json)
    result = generate_bundle(doc, out_dir, opts)
    if args.verbose:
        print(f"[M6] bundle={result.out_dir} files={len(result.files)} total_ms={result.total_ms}")
    return 0

if __name__ == "__main__":
    sys.exit(main())