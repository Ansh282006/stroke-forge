import numpy as np
from ml.metrics import f1, iou, boundary_f1

def test_f1_perfect():
    a = np.zeros((10, 10), np.uint8); a[2:5, 2:5] = 255
    assert f1(a, a) > 0.99

def test_iou_perfect():
    a = np.zeros((10, 10), np.uint8); a[2:5, 2:5] = 255
    assert iou(a, a) > 0.99

def test_f1_disjoint():
    a = np.zeros((10, 10), np.uint8); a[0:2, 0:2] = 255
    b = np.zeros((10, 10), np.uint8); b[5:7, 5:7] = 255
    assert f1(a, b) == 0.0

def test_boundary_f1_range():
    a = np.zeros((20, 20), np.uint8); a[5:15, 5:15] = 255
    b = np.zeros((20, 20), np.uint8); b[5:15, 5:15] = 255
    v = boundary_f1(a, b, tol=1)
    assert 0.0 <= v <= 1.0