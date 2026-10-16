"""Stroke engine CLI (M3)."""
from __future__ import annotations
import argparse, sys
from pathlib import Path
from vectorization.serializer import load
from .orderer import order_paths
from .serializer import save_ordered
from .svg_ordered import save as save_svg

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="StrokeForge stroke engine (M3)")
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args(argv)

    doc = load(args.input)
    doc = order_paths(doc)
    out = Path(args.output); out.mkdir(parents=True, exist_ok=True)
    stem = Path(args.input).stem.replace("_paths", "")
    json_p = save_ordered(doc, out / f"{stem}_ordered.json")
    svg_p = out / f"{stem}_ordered.svg"
    save_svg(doc, svg_p)
    if args.verbose:
        print(f"[M3] paths      : {len(doc.paths)}")
        print(f"[M3] wrote      : {json_p}")
        print(f"[M3] wrote      : {svg_p}")
    return 0

if __name__ == "__main__":
    sys.exit(main())