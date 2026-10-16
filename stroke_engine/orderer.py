"""Heuristic stroke ordering (M3).

Order key (ascending):
  1. hierarchy (outer contours before holes)
  2. -importance (bigger first)
  3. reading order (top-to-bottom, left-to-right) as tiebreaker
"""
from __future__ import annotations
from typing import List
from vectorization.representation import DrawableRepresentation

def order_paths(doc: DrawableRepresentation) -> DrawableRepresentation:
    def key(p):
        cx = p.bbox[0] + p.bbox[2] / 2
        cy = p.bbox[1] + p.bbox[3] / 2
        # bucket y into 20px rows for reading order
        row = int(cy // 20)
        return (p.hierarchy, -p.importance, row, cx)
    ordered = sorted(doc.paths, key=key)
    for i, p in enumerate(ordered, start=1):
        p.order = i
    doc.paths = ordered
    return doc