from vectorization.geometry import polyline_length, polygon_area, bbox, rdp
from vectorization.representation import Path, DrawableRepresentation
from vectorization.extractor import contours_to_paths
from vectorization.svg_renderer import render
import numpy as np

def test_polyline_length():
    assert abs(polyline_length([[0,0],[3,4]]) - 5.0) < 1e-9

def test_polygon_area():
    assert abs(polygon_area([[0,0],[1,0],[1,1],[0,1]]) - 1.0) < 1e-9

def test_bbox():
    assert bbox([[0,0],[2,3]]) == [0, 0, 2, 3]

def test_rdp_reduces_points():
    pts = [[0,0],[1,0.1],[2,0],[3,0.1],[4,0]]
    assert len(rdp(pts, 0.5)) <= len(pts)

def test_extractor_returns_representation():
    c = np.array([[[0,0]],[[10,0]],[[10,10]],[[0,10]]], dtype=np.int32)
    doc = contours_to_paths([c], {"width": 20, "height": 20}, "t.png")
    assert len(doc.paths) == 1
    assert doc.paths[0].length > 0

def test_svg_renderer_contains_path():
    p = Path(id="p0", points=[[0,0],[1,1]], length=1.0)
    doc = DrawableRepresentation(canvas={"width":10,"height":10}, source={"filename":"x"}, paths=[p])
    svg = render(doc)
    assert "<path" in svg and "</svg>" in svg

def test_path_roundtrip():
    p = Path(id="p0", points=[[0,0],[1,1]], length=1.0)
    d = p.to_dict()
    q = Path(**d)
    assert q.id == p.id and q.points == p.points