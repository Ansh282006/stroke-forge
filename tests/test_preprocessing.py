import numpy as np
from preprocessing.config import default_config, load_config
from preprocessing import stages

def _img():
    img = np.zeros((64, 64, 3), dtype=np.uint8)
    img[10:40, 10:40] = 255
    return img

def test_resize_pads_canvas():
    cfg = default_config()
    out = stages.resize(_img(), cfg)
    assert out.shape[0] == cfg.resize.height
    assert out.shape[1] == cfg.resize.width

def test_grayscale_shape():
    g = stages.to_gray(_img())
    assert g.ndim == 2

def test_threshold_binary_range():
    g = stages.to_gray(_img())
    b = stages.threshold(g, default_config())
    assert set(np.unique(b)).issubset({0, 255})

def test_contours_found():
    g = stages.to_gray(_img())
    b = stages.threshold(g, default_config())
    c = stages.find_contours(b)
    assert isinstance(c, list)

def test_load_default_config(tmp_path):
    p = tmp_path / "c.yaml"
    p.write_text("resize:\n  width: 128\n  height: 128\n", encoding="utf-8")
    cfg = load_config(p)
    assert cfg.resize.width == 128