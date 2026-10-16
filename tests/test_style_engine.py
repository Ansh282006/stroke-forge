from style_engine.styles import get_style, list_styles
from style_engine.apply import apply_style
from style_engine.svg_renderer import render

def _doc():
    return {
        "canvas": {"width": 100, "height": 100},
        "paths": [{"id":"p0","points":[[0,0],[10,10]],"length":14.0,"order":1,"closed":False,"area":0.0,"bbox":[0,0,10,10],"hierarchy":0,"is_hole":False,"parent_id":None,"importance":0.5}],
        "timeline": {"total_ms": 300, "entries":[{"path_id":"p0","order":1,"start_ms":0,"duration_ms":300,"end_ms":300,"easing":"easeInOut"}]},
    }

def test_all_styles_exist():
    names = list_styles()
    for n in ["outline","neon","sketch","pencil","lineart","blueprint","particle"]:
        assert n in names

def test_get_unknown_style_raises():
    import pytest
    with pytest.raises(KeyError):
        get_style("nope")

def test_neon_has_glow():
    s = get_style("neon")
    assert s.glow is True

def test_outline_no_glow():
    s = get_style("outline")
    assert s.glow is False

def test_apply_returns_styled_paths():
    s = get_style("outline")
    styled = apply_style(_doc(), s)
    assert len(styled.paths) == 1

def test_render_includes_glow_filter_for_neon():
    s = get_style("neon")
    styled = apply_style(_doc(), s)
    svg = render(styled)
    assert "sf-glow" in svg

def test_render_has_no_glow_for_outline():
    s = get_style("outline")
    styled = apply_style(_doc(), s)
    svg = render(styled)
    assert "sf-glow" not in svg