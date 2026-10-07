"""Tests for the vectorization module."""
from __future__ import annotations

import cv2
import numpy as np
import pytest

from vectorization.extractor import contours_to_paths
from vectorization.geometry import (
    bbox_of,
    polyline_length,
    polygon_area,
    simplify_contour,
)
from vectorization.representation import DrawableRepresentation, Path, Point
from vectorization.serializer import load_json, save_json
from vectorization.svg_renderer import render_svg


@pytest.fixture
def square_image() -> np.ndarray:
    img = np.full((256, 256, 3), 255, dtype=np.uint8)
    img[64:192, 64:192] = 0
    return img


@pytest.fixture
def square_contours(square_image: np.ndarray):
    gray = cv2.cvtColor(square_image, cv2.COLOR_BGR2GRAY)
    _, th = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
    contours, hierarchy = cv2.findContours(
        th, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE
    )
    return contours, hierarchy


def test_simplify_contour_reduces_points(square_contours):
    contours, _ = square_contours
    raw_pts = contours[0].reshape(-1, 2)
    simplified = simplify_contour(contours[0], epsilon_ratio=0.005)
    assert simplified.shape[1] == 2
    assert len(simplified) <= len(raw_pts)


def test_polyline_length_closed_square():
    pts = [(0.0, 0.0), (10.0, 0.0), (10.0, 10.0), (0.0, 10.0)]
    assert polyline_length(pts, closed=True) == pytest.approx(40.0)


def test_polygon_area_square():
    pts = [(0.0, 0.0), (10.0, 0.0), (10.0, 10.0), (0.0, 10.0)]
    assert polygon_area(pts) == pytest.approx(100.0)


def test_bbox_of_square():
    pts = [(0.0, 0.0), (10.0, 0.0), (10.0, 20.0), (0.0, 20.0)]
    assert bbox_of(pts) == (0.0, 0.0, 10.0, 20.0)


def test_contours_to_paths(square_contours):
    contours, hierarchy = square_contours
    paths = contours_to_paths(contours, hierarchy, epsilon_ratio=0.002)
    assert len(paths) >= 1
    p = paths[0]
    assert p.closed is True
    assert p.length > 0
    assert p.area > 0
    assert 0.0 <= p.importance <= 1.0
    assert len(p.points) >= 3


def test_drawable_representation_roundtrip(tmp_path):
    paths = [
        Path(
            id="p0",
            points=[Point(0, 0), Point(10, 0), Point(10, 10)],
            closed=True,
            length=30.0,
            area=50.0,
            bbox=(0.0, 0.0, 10.0, 10.0),
            hierarchy=0,
            is_hole=False,
            parent_id=None,
            importance=0.5,
            order=0,
        )
    ]
    rep = DrawableRepresentation(
        canvas_width=256,
        canvas_height=256,
        paths=paths,
        source_filename="test.png",
    )
    out = tmp_path / "rep.json"
    save_json(rep, out)
    loaded = load_json(out)
    assert loaded.canvas_width == 256
    assert len(loaded.paths) == 1
    assert loaded.paths[0].id == "p0"
    assert loaded.paths[0].points[2].x == 10


def test_svg_renderer_creates_file(tmp_path):
    paths = [
        Path(
            id="p0",
            points=[Point(0, 0), Point(10, 0), Point(10, 10)],
            closed=True,
            length=30.0,
            area=50.0,
            bbox=(0.0, 0.0, 10.0, 10.0),
        )
    ]
    rep = DrawableRepresentation(
        canvas_width=100, canvas_height=100, paths=paths
    )
    out = tmp_path / "out.svg"
    render_svg(rep, out)
    assert out.exists()
    text = out.read_text(encoding="utf-8")
    assert "<svg" in text
    assert "<path" in text
