"""Geometry helpers."""
from __future__ import annotations

import math

import cv2
import numpy as np


def simplify_contour(contour: np.ndarray, epsilon_ratio: float = 0.002) -> np.ndarray:
    if contour.ndim == 3:
        contour = contour.reshape(-1, 2)
    perimeter = cv2.arcLength(contour.reshape(-1, 1, 2), True)
    epsilon = max(1.0, epsilon_ratio * perimeter)
    approx = cv2.approxPolyDP(
        contour.reshape(-1, 1, 2).astype(np.float32), epsilon, True
    )
    return approx.reshape(-1, 2)


def polyline_length(points: list[tuple[float, float]], closed: bool) -> float:
    if len(points) < 2:
        return 0.0
    total = 0.0
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        total += math.hypot(x2 - x1, y2 - y1)
    if closed:
        x1, y1 = points[-1]
        x2, y2 = points[0]
        total += math.hypot(x2 - x1, y2 - y1)
    return total


def polygon_area(points: list[tuple[float, float]]) -> float:
    if len(points) < 3:
        return 0.0
    n = len(points)
    s = 0.0
    for i in range(n):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % n]
        s += x1 * y2 - x2 * y1
    return abs(s) * 0.5


def bbox_of(points: list[tuple[float, float]]) -> tuple[float, float, float, float]:
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)
    return (x_min, y_min, x_max - x_min, y_max - y_min)
