"""Vectorization CLI (M2)."""
from __future__ import annotations
import argparse, sys
from pathlib import Path

from preprocessing.config import load_config, default_config
from preprocessing.pipeline import run as run_pre

from .extractor import contours_to_paths
from .serializer import save as save_json
from .svg_renderer import save as save_svg

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="StrokeForge vectorization (M2)")
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--config", default=None)
    ap.add_argument("--epsilon", type=float, default=1.2)
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args(argv)

    cfg = load_config(args.config) if args.config else default_config()
    pre = run_pre(args.input, cfg)
    doc = contours_to_paths(pre.contours, pre.canvas, pre.filename, epsilon=args.epsilon)

    out_dir = Path(args.output); out_dir.mkdir(parents=True, exist_ok=True)
    stem = Path(args.input).stem
    json_p = save_json(doc, out_dir / f"{stem}_paths.json")
    svg_p = out_dir / f"{stem}_paths.svg"
    save_svg(doc, svg_p)

    if args.verbose:
        print(f"[M2] paths      : {len(doc.paths)}")
        print(f"[M2] wrote      : {json_p}")
        print(f"[M2] wrote      : {svg_p}")
    return 0

if __name__ == "__main__":
    sys.exit(main())