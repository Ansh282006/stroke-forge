"""Contour -> Path extraction (M2)."""
from __future__ import annotations
from typing import List
import cv2, numpy as np

from .representation import Path, DrawableRepresentation
from .geometry import polyline_length, polygon_area, bbox, rdp

def contours_to_paths(contours, canvas, source_name, epsilon=1.2) -> DrawableRepresentation:
    paths: List[Path] = []
    for i, c in enumerate(contours):
        pts = c.reshape(-1, 2).astype(float).tolist()
        if len(pts) < 2: continue
        pts = rdp(pts, epsilon)
        if len(pts) < 2: continue
        length = polyline_length(pts)
        area = polygon_area(pts)
        closed = bool(np.linalg.norm(np.array(pts[0]) - np.array(pts[-1])) < 2.0) if len(pts) > 2 else False
        paths.append(Path(
            id=f"p{i}",
            points=pts,
            closed=closed,
            length=length,
            area=area,
            bbox=bbox(pts),
            importance=0.0,
        ))
    if paths:
        max_len = max(p.length for p in paths) or 1.0
        max_area = max(p.area for p in paths) or 1.0
        for p in paths:
            p.importance = 0.6 * (p.length / max_len) + 0.4 * (p.area / max_area)
    return DrawableRepresentation(
        canvas={"width": canvas["width"], "height": canvas["height"]},
        source={"filename": source_name},
        paths=paths,
        metadata={"num_paths": len(paths)},
    )