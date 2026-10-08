"""Convert OpenCV contours into StrokeForge Path objects."""
from __future__ import annotations

import logging

import numpy as np

from .geometry import bbox_of, polyline_length, polygon_area, simplify_contour
from .representation import Path, Point

logger = logging.getLogger(__name__)


def _hierarchy_lookup(hierarchy: np.ndarray | None, idx: int):
    if hierarchy is None:
        return -1, -1, None
    h = hierarchy[0]
    next_sib, prev_sib, first_child, parent = h[idx]
    return int(next_sib), int(first_child), (int(parent) if parent >= 0 else None)


def _compute_importance(
    area: float, length: float, max_area: float, max_length: float, is_hole: bool
) -> float:
    a = area / max_area if max_area > 0 else 0.0
    l = length / max_length if max_length > 0 else 0.0
    score = 0.6 * a + 0.4 * l
    if is_hole:
        score *= 0.6
    return float(max(0.0, min(1.0, score)))


def contours_to_paths(
    contours: list[np.ndarray],
    hierarchy: np.ndarray | None,
    epsilon_ratio: float = 0.002,
    min_points: int = 3,
) -> list[Path]:
    raw: list[dict] = []

    for idx, contour in enumerate(contours):
        simplified = simplify_contour(contour, epsilon_ratio=epsilon_ratio)
        if len(simplified) < min_points:
            continue

        pts = [(float(x), float(y)) for x, y in simplified.tolist()]
        closed = True
        length = polyline_length(pts, closed=closed)
        area = polygon_area(pts)
        bbox = bbox_of(pts)

        _, _, parent = _hierarchy_lookup(hierarchy, idx)
        is_hole = parent is not None

        raw.append({
            "idx": idx, "points": pts, "closed": closed, "length": length,
            "area": area, "bbox": bbox, "is_hole": is_hole, "parent_idx": parent,
        })

    if not raw:
        return []

    max_area = max(p["area"] for p in raw) or 1.0
    max_length = max(p["length"] for p in raw) or 1.0
    idx_to_id = {p["idx"]: f"p{p['idx']}" for p in raw}

    paths: list[Path] = []
    for p in raw:
        importance = _compute_importance(
            p["area"], p["length"], max_area, max_length, p["is_hole"]
        )
        parent_id = idx_to_id.get(p["parent_idx"]) if p["parent_idx"] is not None else None
        paths.append(Path(
            id=idx_to_id[p["idx"]],
            points=[Point(x=pt[0], y=pt[1]) for pt in p["points"]],
            closed=p["closed"], length=float(p["length"]), area=float(p["area"]),
            bbox=tuple(p["bbox"]),
            hierarchy=1 if p["is_hole"] else 0,
            is_hole=p["is_hole"], parent_id=parent_id,
            importance=importance, order=0,
        ))

    logger.info("Converted %d contours -> %d paths", len(contours), len(paths))
    return paths
