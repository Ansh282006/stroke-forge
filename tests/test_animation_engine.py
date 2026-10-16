import json
import pytest
from animation_engine.timeline import build_animation_timeline, normalize_easing, AnimationTimeline
from animation_engine.svg_animator import render_animated_svg
from animation_engine.player import render_player_html

def _doc():
    return {
        "canvas": {"width": 100, "height": 100},
        "style": {"name":"neon","background":"#000","stroke_color":"#00f0ff","stroke_width":2.0,
                  "opacity":1.0,"linecap":"round","linejoin":"round","glow":True},
        "paths": [
            {"id":"p0","points":[[0,0],[10,10],[20,0]],"length":30.0,"order":1},
            {"id":"p1","points":[[20,0],[30,10]],"length":15.0,"order":2},
        ],
        "timeline": {"total_ms":600,"entries":[
            {"path_id":"p0","order":1,"start_ms":0,"duration_ms":300,"end_ms":300,"easing":"easeInOut"},
            {"path_id":"p1","order":2,"start_ms":300,"duration_ms":300,"end_ms":600,"easing":"linear"},
        ]},
    }

def test_normalize_easing_variants():
    assert normalize_easing("easeInOut") == "ease-in-out"
    assert normalize_easing(None) == "ease-in-out"

def test_build_timeline_basic():
    tl = build_animation_timeline(_doc())
    assert isinstance(tl, AnimationTimeline)
    assert len(tl.entries) == 2 and tl.total_ms == 600

def test_build_timeline_speed():
    tl = build_animation_timeline(_doc(), speed=2.0)
    assert tl.entries[0].duration_ms == 150 and tl.total_ms == 300

def test_build_timeline_gap():
    tl = build_animation_timeline(_doc(), gap_ms=100)
    assert tl.total_ms == 700

def test_build_timeline_fallback():
    doc = _doc(); doc.pop("timeline")
    tl = build_animation_timeline(doc)
    assert len(tl.entries) == 2 and tl.total_ms > 0

def test_speed_must_be_positive():
    with pytest.raises(ValueError):
        build_animation_timeline(_doc(), speed=0)

def test_animated_svg_keyframes_and_vars():
    doc = _doc(); tl = build_animation_timeline(doc)
    svg = render_animated_svg(doc, tl)
    assert "@keyframes sf-draw" in svg and "stroke-dashoffset" in svg
    assert "--sf-len:30.00" in svg and "--sf-dur:300ms" in svg

def test_player_wraps_with_controls():
    doc = _doc(); tl = build_animation_timeline(doc)
    svg = render_animated_svg(doc, tl, autoplay=True)
    html = render_player_html(svg, title="Demo", total_ms=tl.total_ms)
    for token in ["<!doctype html>", "sf-playpause", "sf-restart", "sf-speed", "getAnimations"]:
        assert token in html

def test_cli_end_to_end(tmp_path):
    from animation_engine.cli import main as cli
    p = tmp_path / "face_neon.json"; p.write_text(json.dumps(_doc()), encoding="utf-8")
    out = tmp_path / "out"
    assert cli(["--input", str(p), "--output", str(out)]) == 0
    assert (out / "face_neon_player.html").exists()