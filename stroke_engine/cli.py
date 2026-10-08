"""CLI: unordered JSON -> ordered JSON + ordered SVG."""
from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

from vectorization.serializer import load_json

from .orderer import order_paths
from .serializer import save_ordered
from .svg_ordered import render_svg_ordered
from .timeline import build_timeline


def setup_logging(verbose: bool) -> None:
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
        datefmt="%H:%M:%S",
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="stroke_engine.cli")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("data/outputs"))
    parser.add_argument("--total-ms", type=int, default=4500)
    parser.add_argument("--min-ms", type=int, default=120)
    parser.add_argument("--max-ms", type=int, default=900)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args(argv)

    setup_logging(args.verbose)
    logger = logging.getLogger("stroke-forge.stroke_engine")

    if not args.input.exists():
        logger.error("Input JSON not found: %s", args.input)
        return 2

    rep = load_json(args.input)
    ordered = order_paths(rep.paths)
    rep.paths = ordered

    timeline, total_ms = build_timeline(
        ordered, total_duration_ms=args.total_ms,
        min_duration_ms=args.min_ms, max_duration_ms=args.max_ms,
    )

    args.output.mkdir(parents=True, exist_ok=True)
    stem = args.input.stem.replace("_paths", "")
    ordered_json = args.output / f"{stem}_ordered.json"
    ordered_svg = args.output / f"{stem}_ordered.svg"

    save_ordered(rep, timeline, total_ms, ordered_json)
    render_svg_ordered(rep, ordered_svg)

    logger.info("Wrote %s", ordered_json)
    logger.info("Wrote %s", ordered_svg)
    logger.info("Total animation: %d ms across %d paths", total_ms, len(ordered))
    return 0


if __name__ == "__main__":
    sys.exit(main())
