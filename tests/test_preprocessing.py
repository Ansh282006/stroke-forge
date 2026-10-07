"""Unit tests for the preprocessing pipeline."""
from __future__ import annotations

import numpy as np
import pytest

from preprocessing.config import PreprocessConfig
from preprocessing.pipeline import run_pipeline


@pytest.fixture
def square_image() -> np.ndarray:
    img = np.full((256, 256, 3), 255, dtype=np.uint8)
    img[64:192, 64:192] = 0
    return img


def test_pipeline_returns_expected_shapes(square_image: np.ndarray) -> None:
    result = run_pipeline(square_image, PreprocessConfig())
    assert result.original.shape[:2] == (256, 256)
    assert result.grayscale.shape == (256, 256)
    assert result.canny.shape == (256, 256)
    assert result.skeleton.shape == (256, 256)
    assert isinstance(result.contours, list)
    assert result.metadata["processed_shape"][:2] == (256, 256)


def test_at_least_one_contour_on_square(square_image: np.ndarray) -> None:
    result = run_pipeline(square_image, PreprocessConfig())
    assert len(result.contours) >= 1


def test_resize_applied_to_large_image() -> None:
    img = np.full((2048, 1024, 3), 255, dtype=np.uint8)
    img[100:200, 100:200] = 0
    result = run_pipeline(img, PreprocessConfig())
    assert max(result.original.shape[:2]) <= 1024


def test_empty_image_raises() -> None:
    with pytest.raises(ValueError):
        run_pipeline(np.array([]), PreprocessConfig())


def test_metadata_contains_elapsed() -> None:
    img = np.full((128, 128, 3), 255, dtype=np.uint8)
    img[40:80, 40:80] = 0
    result = run_pipeline(img, PreprocessConfig())
    assert "elapsed_ms" in result.metadata
    assert result.metadata["elapsed_ms"] >= 0.0
