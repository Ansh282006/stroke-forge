from vectorization.representation import Path, DrawableRepresentation
from stroke_engine.orderer import order_paths
from stroke_engine.timeline import build_timeline

def _doc():
    return DrawableRepresentation(
        canvas={"width": 100, "height": 100},
        source={"filename": "x"},
        paths=[
            Path(id="p2", points=[[0,0],[10,0]], length=10, importance=0.2, bbox=[0,0,10,0]),
            Path(id="p1", points=[[0,0],[30,0]], length=30, importance=0.9, bbox=[0,0,30,0]),
            Path(id="p0", points=[[0,0],[5,0]], length=5,  importance=0.5, bbox=[0,0,5,0]),
        ],
    )

def test_order_assigns_sequential_orders():
    doc = order_paths(_doc())
    assert [p.order for p in doc.paths] == [1, 2, 3]

def test_order_places_higher_importance_first():
    doc = order_paths(_doc())
    assert doc.paths[0].id == "p1"

def test_timeline_total_matches_sum():
    doc = order_paths(_doc())
    tl = build_timeline(doc)
    assert tl["total_ms"] == sum(e["duration_ms"] for e in tl["entries"])

def test_timeline_min_duration():
    doc = order_paths(_doc())
    tl = build_timeline(doc)
    for e in tl["entries"]:
        assert e["duration_ms"] >= 120

def test_timeline_max_duration():
    doc = DrawableRepresentation(
        canvas={"width": 100, "height": 100}, source={"filename": "x"},
        paths=[Path(id="p0", points=[[0,0],[10000,0]], length=10000, importance=1.0, bbox=[0,0,10000,0])],
    )
    doc = order_paths(doc)
    tl = build_timeline(doc)
    assert tl["entries"][0]["duration_ms"] <= 1200

def test_order_reading_top_to_bottom():
    doc = DrawableRepresentation(
        canvas={"width": 200, "height": 200}, source={"filename": "x"},
        paths=[
            Path(id="bottom", points=[[0,100],[10,100]], length=10, importance=0.5, bbox=[0,100,10,0]),
            Path(id="top",    points=[[0,10], [10,10]],  length=10, importance=0.5, bbox=[0,10,10,0]),
        ],
    )
    doc = order_paths(doc)
    assert doc.paths[0].id == "top"

def test_ordered_json_contains_timeline(tmp_path):
    from stroke_engine.serializer import save_ordered
    import json
    doc = order_paths(_doc())
    p = save_ordered(doc, tmp_path / "o.json")
    data = json.loads(p.read_text(encoding="utf-8"))
    assert "timeline" in data and "entries" in data["timeline"]

def test_multiple_paths_get_distinct_orders():
    doc = order_paths(_doc())
    orders = [p.order for p in doc.paths]
    assert len(set(orders)) == len(orders)

def test_timeline_entries_sorted_by_order():
    doc = order_paths(_doc())
    tl = build_timeline(doc)
    orders = [e["order"] for e in tl["entries"]]
    assert orders == sorted(orders)