"""Deterministic, parent-aware stroke ordering."""
from __future__ import annotations

import logging
from typing import Literal

from vectorization.representation import Path

from .features import PathFeatures, extract_features

logger = logging.getLogger(__name__)

OrderStrategy = Literal["importance", "length", "reading"]


def _strategy_key(
    features: PathFeatures,
    strategy: OrderStrategy,
) -> tuple:
    """Return deterministic sibling-ranking keys."""
    if strategy == "length":
        return (
            -features.length,
            -features.importance,
            round(features.top, 3),
            round(features.left, 3),
            features.id,
        )

    if strategy == "reading":
        return (
            round(features.top, 3),
            round(features.left, 3),
            -features.importance,
            -features.length,
            features.id,
        )

    return (
        -features.importance,
        -features.length,
        round(features.top, 3),
        round(features.left, 3),
        features.id,
    )


def _eligible_sort_key(
    features: PathFeatures,
    strategy: OrderStrategy,
) -> tuple:
    """Rank currently eligible paths.

    Non-hole/outer paths are preferred over holes. The parent-child
    constraint itself is enforced by the ordering loop.
    """
    hole_rank = 1 if features.is_hole or features.hierarchy > 0 else 0
    return (
        hole_rank,
        *_strategy_key(features, strategy),
    )


def order_paths(
    paths: list[Path],
    strategy: OrderStrategy = "importance",
) -> list[Path]:
    """Order paths while respecting parent-before-child constraints.

    A path becomes eligible when its parent has already been ordered or
    when its parent reference is missing from the current path set.

    The algorithm is deterministic and handles broken/cyclic references
    by falling back to the remaining candidates.
    """
    if not paths:
        return []

    if strategy not in {"importance", "length", "reading"}:
        raise ValueError(
            f"Unknown ordering strategy: {strategy}. "
            "Expected: importance, length, or reading."
        )

    features_by_id: dict[str, PathFeatures] = {
        path.id: extract_features(path)
        for path in paths
    }
    path_by_id: dict[str, Path] = {
        path.id: path
        for path in paths
    }

    remaining: set[str] = set(path_by_id)
    ordered: list[Path] = []

    while remaining:
        eligible_ids = []

        for path_id in remaining:
            path = path_by_id[path_id]
            parent_id = path.parent_id

            if parent_id is None or parent_id not in remaining:
                eligible_ids.append(path_id)

        # Broken/cyclic hierarchy references should never block the engine.
        if not eligible_ids:
            logger.warning(
                "Hierarchy cycle or unresolved dependency detected; "
                "falling back to remaining paths."
            )
            eligible_ids = list(remaining)

        eligible_ids.sort(
            key=lambda path_id: _eligible_sort_key(
                features_by_id[path_id],
                strategy,
            )
        )

        selected_id = eligible_ids[0]
        selected_path = path_by_id[selected_id]

        selected_path.order = len(ordered) + 1
        ordered.append(selected_path)
        remaining.remove(selected_id)

    logger.info(
        "Ordered %d paths using '%s' strategy",
        len(ordered),
        strategy,
    )

    return ordered
