import json
from code_generator.options import GeneratorOptions
from code_generator.generator import generate_bundle, BundleResult
from code_generator.css_builder import build_css
from code_generator.tailwind_config import build_tailwind_config
from code_generator.js_builder import build_js
from code_generator.html_builder import build_html
from animation_engine.timeline import build_animation_timeline

def _doc():
    return {
        "canvas": {"width": 100, "height": 100},
        "style": {"name":"neon","background":"#000","stroke_color":"#00f0ff","stroke_width":2.0,
                  "opacity":1.0,"linecap":"round","linejoin":"round","glow":True},
        "paths": [{"id":"p0","points":[[0,0],[10,10]],"length":14.0,"order":1}],
        "timeline": {"total_ms":300,"entries":[
            {"path_id":"p0","order":1,"start_ms":0,"duration_ms":300,"end_ms":300,"easing":"easeInOut"}]},
    }

def test_css_has_keyframes():
    css = build_css(_doc())
    assert "@keyframes sf-draw" in css and ".sf-path" in css

def test_tailwind_config_is_json_like():
    tw = build_tailwind_config(_doc())
    body = tw.split("tailwind.config = ", 1)[1].rstrip().rstrip(";")
    parsed = json.loads(body)
    assert "theme" in parsed

def test_js_embeds_payload():
    doc = _doc(); tl = build_animation_timeline(doc)
    js = build_js(doc, tl, GeneratorOptions().to_dict())
    payload = js.split("const SF_DATA = ", 1)[1].split(";\n", 1)[0]
    parsed = json.loads(payload)
    assert "paths" in parsed and "timeline" in parsed

def test_html_references_bundle_files():
    html = build_html(_doc(), GeneratorOptions(title="Demo"))
    for t in ['<title>Demo</title>', 'href="styles.css"', 'src="script.js"', 'id="sf-stage"']:
        assert t in html

def test_generate_bundle_writes_all_files(tmp_path):
    res = generate_bundle(_doc(), tmp_path, GeneratorOptions(name="d"))
    assert isinstance(res, BundleResult)
    names = sorted(p.name for p in res.files)
    for f in ["index.html","styles.css","script.js","tailwind.config.js","data.json","README.md"]:
        assert f in names

def test_generate_bundle_skip_flags(tmp_path):
    res = generate_bundle(_doc(), tmp_path, GeneratorOptions(name="d", include_readme=False, include_animation_json=False))
    names = sorted(p.name for p in res.files)
    assert "README.md" not in names and "data.json" not in names

def test_cli_end_to_end(tmp_path):
    from code_generator.cli import main as cli
    p = tmp_path / "face_neon.json"; p.write_text(json.dumps(_doc()), encoding="utf-8")
    out = tmp_path / "web"
    assert cli(["--input", str(p), "--output", str(out), "--name", "face_neon"]) == 0
    assert (out / "face_neon" / "index.html").exists()