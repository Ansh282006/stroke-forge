"""Pairwise stroke-ordering model (M11). Skeleton."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass
class OrderFeatures:
    len_a: float
    len_b: float
    area_a: float
    area_b: float
    y_a: float
    y_b: float
    x_a: float
    x_b: float

def score_pair(f: OrderFeatures) -> float:
    """Return p(A before B). Heuristic stub until M11 model is trained."""
    import math
    # reading-order bias + size bias
    y_term = math.tanh((f.y_b - f.y_a) / 20.0) * 0.6
    s_term = math.tanh((f.len_a - f.len_b) / 40.0) * 0.2
    return 0.5 + 0.4 * y_term + 0.2 * s_term