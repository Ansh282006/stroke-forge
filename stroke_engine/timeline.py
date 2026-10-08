"""Timeline generation from ordered paths."""
from __future__ import annotations

import logging
from dataclasses import dataclass

from vectorization.representation import Path

logger = logging.getLogger(__name__)


@dataclass
class TimelineEntry:
    path_id: str
    order: int
    start_ms: int
    duration_ms: int
    end_ms: int
    easing: str


def build_timeline(
    paths: list[Path],
    total_duration_ms: int = 4500,
    min_duration_ms: int = 120,
    max_duration_ms: int = 900,
    default_easing: str = "easeInOut",
) -> tuple[list[TimelineEntry], int]:
    if not paths:
        return [], 0
    ordered = sorted(paths, key=lambda p: p.order)
    lengths = [max(p.length, 1e-6) for p in ordered]
    total_length = sum(lengths)
    raw = [total_duration_ms * (l / total_length) for l in lengths]
    clamped = [int(max(min_duration_ms, min(max_duration_ms, d))) for d in raw]
    entries: list[TimelineEntry] = []
    cursor = 0
    for path, dur in zip(ordered, clamped):
        entries.append(TimelineEntry(
            path_id=path.id, order=path.order,
            start_ms=cursor, duration_ms=dur, end_ms=cursor + dur,
            easing=default_easing,
        ))
        cursor += dur
    logger.info("Timeline built | %d entries | total %d ms", len(entries), cursor)
    return entries, cursor
