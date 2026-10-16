"""Pipeline orchestrator (M1)."""
from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional
import cv2
import numpy as np

from .config import PreprocessConfig, load_config, default_config
from . import stages

@dataclass
class PreprocessResult:
    filename: str
    canvas: Dict[str, int]
    stages: Dict[str, np.ndarray] = field(default_factory=dict)
    contours: List[Any] = field(default_factory=list)
    binary: Optional[np.ndarray] = None
    edges: Optional[np.ndarray] = None
    gray: Optional[np.ndarray] = None

def run(image_path, config: Optional[PreprocessConfig] = None) -> PreprocessResult:
    cfg = config or default_config()
    img = cv2.imread(str(image_path), cv2.IMREAD_COLOR)
    if img is None: raise FileNotFoundError(f"cannot read {image_path}")

    st: Dict[str, np.ndarray] = {}
    st["original"] = img.copy()
    img = stages.resize(img, cfg); st["resize"] = img.copy()
    g = stages.to_gray(img);     st["gray"] = g.copy()
    g = stages.denoise(g, cfg);  st["denoise"] = g.copy()
    g = stages.contrast(g, cfg); st["contrast"] = g.copy()
    b = stages.threshold(g, cfg); st["threshold"] = b.copy()
    e = stages.edges(g, cfg);    st["edges"] = e.copy()
    closed = stages.morphology_close(b, cfg); st["close"] = closed.copy()
    sk = stages.skeletonize(closed, cfg);     st["skeleton"] = sk.copy()
    cts = stages.find_contours(closed)
    cts = [c for c in cts if cv2.contourArea(c) >= cfg.contours.min_area]

    h, w = img.shape[:2]
    return PreprocessResult(
        filename=Path(image_path).name,
        canvas={"width": w, "height": h},
        stages=st, contours=cts,
        binary=closed, edges=e, gray=g,
    )