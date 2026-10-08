"""Heuristic stroke ordering."""
from __future__ import annotations

import logging

from vectorization.representation import Path

from .features import PathFeatures, extract_features

logger = logging.getLogger(__name__)


def _sort_key(f: PathFeatures) -> tuple:
    return (f.hierarchy, -f.importance, -f.length,
            round(f.top, 3), round(f.left, 3), f.id)


def order_paths(paths: list[Path]) -> list[Path]:
    if not paths:
        return []
    features = [extract_features(p) for p in paths]
    paired = list(zip(features, paths))
    paired.sort(key=lambda pair: _sort_key(pair[0]))
    ordered: list[Path] = []
    for seq, (_, path) in enumerate(paired, start=1):
        path.order = seq
        ordered.append(path)
    logger.info("Ordered %d paths", len(ordered))
    return ordered
