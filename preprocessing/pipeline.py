"""Orchestrates preprocessing stages into a single reproducible run."""
from __future__ import annotations

import logging
import time
from dataclasses import dataclass
from typing import Any

import cv2
import numpy as np

from . import stages
from .config import PreprocessConfig

logger = logging.getLogger(__name__)


@dataclass
class PreprocessResult:
    original: np.ndarray
    grayscale: np.ndarray
    denoised: np.ndarray
    enhanced: np.ndarray
    otsu: np.ndarray
    adaptive: np.ndarray
    canny: np.ndarray
    closed_edges: np.ndarray
    skeleton: np.ndarray
    contours: list[np.ndarray]
    contour_overlay: np.ndarray
    metadata: dict[str, Any]


def run_pipeline(image: np.ndarray, config: PreprocessConfig) -> PreprocessResult:
    t0 = time.perf_counter()

    if image is None or image.size == 0:
        raise ValueError("Empty or None image passed to run_pipeline")

    original = stages.resize_max(image, config.resize.max_side)
    logger.debug("Resized to shape %s", original.shape)

    gray = stages.to_grayscale(original)

    denoised = stages.denoise_bilateral(
        gray,
        d=config.bilateral.d,
        sigma_color=config.bilateral.sigma_color,
        sigma_space=config.bilateral.sigma_space,
    )

    if config.clahe.enabled:
        enhanced = stages.apply_clahe(
            denoised, config.clahe.clip_limit, config.clahe.grid_size
        )
    else:
        enhanced = denoised

    otsu = stages.otsu_threshold(enhanced, invert=config.otsu.invert)
    adaptive = stages.adaptive_threshold(
        enhanced,
        block=config.adaptive.block_size,
        c=config.adaptive.c,
        invert=config.adaptive.invert,
    )

    canny = stages.canny_edges(
        enhanced, config.canny.low, config.canny.high, config.canny.aperture
    )
    closed = stages.morphological_close(
        canny, config.morphology.kernel_size, config.morphology.iterations
    )

    skeleton = stages.skeletonize_binary(closed)

    contours, _ = stages.find_contours(closed, config.contours.min_area)

    overlay = original.copy()
    if overlay.ndim == 2:
        overlay = cv2.cvtColor(overlay, cv2.COLOR_GRAY2BGR)
    cv2.drawContours(overlay, contours, -1, (0, 255, 0), 1)

    elapsed = time.perf_counter() - t0
    metadata = {
        "original_shape": tuple(image.shape),
        "processed_shape": tuple(original.shape),
        "num_contours": len(contours),
        "elapsed_ms": round(elapsed * 1000, 2),
    }
    logger.info(
        "Pipeline done in %.2f ms | %d contours | processed %s",
        elapsed * 1000,
        len(contours),
        original.shape,
    )

    return PreprocessResult(
        original=original,
        grayscale=gray,
        denoised=denoised,
        enhanced=enhanced,
        otsu=otsu,
        adaptive=adaptive,
        canny=canny,
        closed_edges=closed,
        skeleton=skeleton,
        contours=contours,
        contour_overlay=overlay,
        metadata=metadata,
    )
