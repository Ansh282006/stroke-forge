"""Geometry utilities (M2)."""
from __future__ import annotations
import math
from typing import List, Sequence

def polyline_length(points: Sequence[Sequence[float]]) -> float:
    t = 0.0
    for i in range(1, len(points)):
        dx = points[i][0] - points[i-1][0]
        dy = points[i][1] - points[i-1][1]
        t += math.hypot(dx, dy)
    return t

def polygon_area(points: Sequence[Sequence[float]]) -> float:
    n = len(points)
    if n < 3: return 0.0
    s = 0.0
    for i in range(n):
        j = (i + 1) % n
        s += points[i][0] * points[j][1] - points[j][0] * points[i][1]
    return abs(s) * 0.5

def bbox(points: Sequence[Sequence[float]]) -> List[float]:
    if not points: return [0.0, 0.0, 0.0, 0.0]
    xs = [p[0] for p in points]; ys = [p[1] for p in points]
    x0, x1 = min(xs), max(xs); y0, y1 = min(ys), max(ys)
    return [x0, y0, x1 - x0, y1 - y0]

def _perp_dist(p, a, b) -> float:
    if a == b:
        return math.hypot(p[0] - a[0], p[1] - a[1])
    num = abs((b[0]-a[0])*(a[1]-p[1]) - (a[0]-p[0])*(b[1]-a[1]))
    den = math.hypot(b[0]-a[0], b[1]-a[1])
    return num / den if den else 0.0

def rdp(points: List[List[float]], epsilon: float) -> List[List[float]]:
    if len(points) < 3: return points[:]
    a, b = points[0], points[-1]
    dmax, idx = 0.0, 0
    for i in range(1, len(points) - 1):
        d = _perp_dist(points[i], a, b)
        if d > dmax: dmax, idx = d, i
    if dmax > epsilon:
        left = rdp(points[:idx+1], epsilon)
        right = rdp(points[idx:], epsilon)
        return left[:-1] + right
    return [a, b]