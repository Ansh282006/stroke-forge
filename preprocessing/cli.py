"""Preprocessing CLI (M1)."""
from __future__ import annotations
import argparse, sys
from pathlib import Path
from .config import load_config, default_config
from .pipeline import run
from .visualize import save_stage_grid

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="StrokeForge preprocessing (M1)")
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--config", default=None)
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args(argv)

    cfg = load_config(args.config) if args.config else default_config()
    res = run(args.input, cfg)
    out_dir = Path(args.output); out_dir.mkdir(parents=True, exist_ok=True)
    stem = Path(args.input).stem
    grid = save_stage_grid(res, out_dir / f"{stem}_stages.png")
    if args.verbose:
        print(f"[M1] input      : {args.input}")
        print(f"[M1] canvas     : {res.canvas}")
        print(f"[M1] contours   : {len(res.contours)}")
        print(f"[M1] wrote      : {grid}")
    return 0

if __name__ == "__main__":
    sys.exit(main())