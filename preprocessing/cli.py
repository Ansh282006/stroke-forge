"""Command-line entry point for the preprocessing pipeline."""
from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

import cv2

from .config import PreprocessConfig
from .pipeline import run_pipeline
from .visualize import plot_stages


def setup_logging(verbose: bool) -> None:
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
        datefmt="%H:%M:%S",
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="preprocessing.cli",
        description="Run the StrokeForge preprocessing pipeline on an image.",
    )
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=Path("data/outputs"))
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("configs/preprocessing.yaml"),
    )
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args(argv)

    setup_logging(args.verbose)
    logger = logging.getLogger("stroke-forge.cli")

    if not args.input.exists():
        logger.error("Input image not found: %s", args.input)
        return 2

    if args.config.exists():
        config = PreprocessConfig.from_yaml(args.config)
        logger.info("Loaded config from %s", args.config)
    else:
        config = PreprocessConfig()
        logger.warning("Config not found, using defaults: %s", args.config)

    image = cv2.imread(str(args.input), cv2.IMREAD_UNCHANGED)
    if image is None:
        logger.error("Failed to read image: %s", args.input)
        return 3

    result = run_pipeline(image, config)

    args.output.mkdir(parents=True, exist_ok=True)
    plot_path = args.output / f"{args.input.stem}_stages.png"
    plot_stages(result, plot_path, title=f"Preprocessing: {args.input.name}")
    logger.info("Wrote stage grid: %s", plot_path)
    logger.info("Contours: %d", len(result.contours))
    logger.info("Metadata: %s", result.metadata)
    return 0


if __name__ == "__main__":
    sys.exit(main())
