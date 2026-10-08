"""Tests for parent-aware stroke ordering and strategy selection."""
from __future__ import annotations

from stroke_engine.orderer import order_paths
from vectorization.representation import Path, Point


def _mk_path(
    pid: str,
    importance: float,
    length: float,
    bbox: tuple[float, float, float, float],
    *,
    is_hole: bool = False,
    parent_id: str | None = None,
) -> Path:
    return Path(
        id=pid,
        points=[
            Point(bbox[0], bbox[1]),
            Point(
                bbox[0] + bbox[2],
                bbox[1] + bbox[3],
            ),
        ],
        closed=True,
        length=length,
        area=bbox[2] * bbox[3],
        bbox=bbox,
        hierarchy=1 if is_hole else 0,
        is_hole=is_hole,
        parent_id=parent_id,
        importance=importance,
        order=0,
    )


def test_parent_is_ordered_before_child() -> None:
    parent = _mk_path(
        "parent",
        importance=0.2,
        length=50,
        bbox=(0, 0, 100, 100),
    )
    child = _mk_path(
        "child",
        importance=1.0,
        length=500,
        bbox=(10, 10, 20, 20),
        is_hole=True,
        parent_id="parent",
    )

    ordered = order_paths(
        [child, parent],
        strategy="importance",
    )

    assert [p.id for p in ordered] == [
        "parent",
        "child",
    ]


def test_length_strategy_changes_sibling_priority() -> None:
    short = _mk_path(
        "short",
        importance=0.9,
        length=20,
        bbox=(0, 0, 10, 10),
    )
    long = _mk_path(
        "long",
        importance=0.1,
        length=500,
        bbox=(100, 100, 50, 50),
    )

    ordered = order_paths(
        [short, long],
        strategy="length",
    )

    assert [p.id for p in ordered] == [
        "long",
        "short",
    ]


def test_reading_strategy_prioritizes_top_left() -> None:
    bottom = _mk_path(
        "bottom",
        importance=1.0,
        length=500,
        bbox=(0, 200, 50, 50),
    )
    top = _mk_path(
        "top",
        importance=0.1,
        length=10,
        bbox=(0, 0, 50, 50),
    )

    ordered = order_paths(
        [bottom, top],
        strategy="reading",
    )

    assert [p.id for p in ordered] == [
        "top",
        "bottom",
    ]


def test_invalid_strategy_raises() -> None:
    path = _mk_path(
        "p0",
        importance=0.5,
        length=100,
        bbox=(0, 0, 10, 10),
    )

    try:
        order_paths(
            [path],
            strategy="invalid",  # type: ignore[arg-type]
        )
    except ValueError as exc:
        assert "Unknown ordering strategy" in str(exc)
    else:
        raise AssertionError("Expected ValueError")
