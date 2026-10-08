"""Tests for the stroke-ordering and timeline modules."""
from __future__ import annotations

from stroke_engine.orderer import order_paths
from stroke_engine.timeline import build_timeline
from vectorization.representation import Path, Point


def _mk_path(pid, importance, length, bbox, is_hole=False):
    return Path(
        id=pid,
        points=[Point(bbox[0], bbox[1]), Point(bbox[0] + bbox[2], bbox[1] + bbox[3])],
        closed=True, length=length, area=bbox[2] * bbox[3], bbox=bbox,
        hierarchy=1 if is_hole else 0, is_hole=is_hole,
        parent_id=None, importance=importance, order=0,
    )


def test_order_puts_outer_before_hole():
    outer = _mk_path("outer", 0.9, 400, (0, 0, 100, 100))
    hole = _mk_path("hole", 0.9, 400, (10, 10, 10, 10), is_hole=True)
    assert [p.id for p in order_paths([hole, outer])] == ["outer", "hole"]


def test_order_by_importance_desc():
    a = _mk_path("a", 0.9, 400, (0, 0, 100, 100))
    b = _mk_path("b", 0.3, 400, (200, 200, 100, 100))
    assert [p.id for p in order_paths([b, a])] == ["a", "b"]


def test_order_by_length_tiebreak():
    short = _mk_path("short", 0.5, 50, (0, 0, 10, 10))
    long_ = _mk_path("long", 0.5, 500, (100, 100, 50, 50))
    assert order_paths([short, long_])[0].id == "long"


def test_order_by_reading_order():
    top = _mk_path("top", 0.5, 100, (0, 0, 50, 50))
    bottom = _mk_path("bottom", 0.5, 100, (0, 100, 50, 50))
    assert order_paths([bottom, top])[0].id == "top"


def test_order_sets_sequence_numbers():
    a = _mk_path("a", 0.9, 400, (0, 0, 100, 100))
    b = _mk_path("b", 0.3, 100, (200, 200, 100, 100))
    assert [p.order for p in order_paths([b, a])] == [1, 2]


def test_order_is_deterministic():
    a = _mk_path("a", 0.5, 100, (0, 0, 50, 50))
    b = _mk_path("b", 0.5, 100, (0, 0, 50, 50))
    assert [p.id for p in order_paths([a, b])] == [p.id for p in order_paths([b, a])]


def test_timeline_respects_total_duration():
    paths = [_mk_path(f"p{i}", 0.5, 100.0 * (i + 1), (0, 0, 10, 10)) for i in range(5)]
    ordered = order_paths(paths)
    entries, total = build_timeline(ordered, 4000, 100, 1000)
    assert len(entries) == 5
    assert total == sum(e.duration_ms for e in entries)
    assert entries[0].start_ms == 0


def test_timeline_empty():
    assert build_timeline([]) == ([], 0)


def test_timeline_clamps_min_max():
    paths = [_mk_path("tiny", 0.5, 1e-6, (0, 0, 1, 1)),
             _mk_path("huge", 0.5, 1e9, (0, 0, 1, 1))]
    ordered = order_paths(paths)
    entries, _ = build_timeline(ordered, 5000, 150, 500)
    durations = {e.path_id: e.duration_ms for e in entries}
    assert durations["huge"] <= 500
    assert durations["tiny"] >= 150
