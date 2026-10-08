"""CLI: image -> DrawableRepresentation (JSON) + SVG preview."""
from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

import cv2

from preprocessing.config import PreprocessConfig
from preprocessing.pipeline import run_pipeline

from .extractor import contours_to_paths
from .representation import DrawableRepresentation
from .serializer import save_json
from .svg_renderer import render_svg


def setup_logging(verbose: bool) -> None:
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
        datefmt="%H:%M:%S",
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="vectorization.cli")
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("data/outputs"))
    parser.add_argument("--config", type=Path, default=Path("configs/preprocessing.yaml"))
    parser.add_argument("--epsilon", type=float, default=0.002)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args(argv)

    setup_logging(args.verbose)
    logger = logging.getLogger("stroke-forge.vectorization")

    if not args.input.exists():
        logger.error("Input image not found: %s", args.input)
        return 2

    config = PreprocessConfig.from_yaml(args.config) if args.config.exists() else PreprocessConfig()

    image = cv2.imread(str(args.input), cv2.IMREAD_UNCHANGED)
    if image is None:
        logger.error("Failed to read image: %s", args.input)
        return 3

    result = run_pipeline(image, config)
    h, w = result.original.shape[:2]

    paths = contours_to_paths(result.contours, hierarchy=None, epsilon_ratio=args.epsilon)

    rep = DrawableRepresentation(
        canvas_width=w, canvas_height=h, paths=paths,
        source_filename=args.input.name,
        metadata={"num_paths": len(paths), "preprocess": result.metadata},
    )

    args.output.mkdir(parents=True, exist_ok=True)
    json_path = args.output / f"{args.input.stem}_paths.json"
    svg_path = args.output / f"{args.input.stem}_paths.svg"

    save_json(rep, json_path)
    render_svg(rep, svg_path)

    logger.info("Wrote %s (%d paths)", json_path, len(paths))
    logger.info("Wrote %s", svg_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
