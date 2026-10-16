"""Edge metrics (M9)."""
from __future__ import annotations
import numpy as np

def _bin(x, thr=127):
    return (x > thr).astype(np.uint8)

def f1(pred, target, thr=127) -> float:
    p, t = _bin(pred, thr), _bin(target, thr)
    tp = int(((p == 1) & (t == 1)).sum())
    fp = int(((p == 1) & (t == 0)).sum())
    fn = int(((p == 0) & (t == 1)).sum())
    if tp == 0: return 0.0
    prec = tp / (tp + fp)
    rec  = tp / (tp + fn)
    return 2 * prec * rec / (prec + rec) if (prec + rec) else 0.0

def iou(pred, target, thr=127) -> float:
    p, t = _bin(pred, thr), _bin(target, thr)
    inter = int(((p == 1) & (t == 1)).sum())
    union = int(((p == 1) | (t == 1)).sum())
    return inter / union if union else 0.0

def boundary_f1(pred, target, tol=2, thr=127) -> float:
    import cv2
    p, t = _bin(pred, thr) * 255, _bin(target, thr) * 255
    k = np.ones((2 * tol + 1, 2 * tol + 1), np.uint8)
    pd = cv2.dilate(p, k); td = cv2.dilate(t, k)
    prec = ((p > 0) & (td > 0)).sum() / max(1, (p > 0).sum())
    rec  = ((t > 0) & (pd > 0)).sum() / max(1, (t > 0).sum())
    return float(2 * prec * rec / (prec + rec)) if (prec + rec) else 0.0