"""Edge dataset (M9) — image -> (image, canny-edge) pairs.

This is the *baseline* dataset: targets are produced by the same Canny
stage used in M1, so a model trained here will at best match Canny.
M10 will replace targets with hand-labeled edges.
"""
from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import List, Tuple
import cv2
import numpy as np

@dataclass
class Pair:
    image_path: Path
    edge_path: Path

def build_pairs(samples_dir: Path, out_dir: Path) -> List[Pair]:
    samples_dir, out_dir = Path(samples_dir), Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    pairs: List[Pair] = []
    for img_p in sorted(samples_dir.glob("*.png")):
        img = cv2.imread(str(img_p), cv2.IMREAD_GRAYSCALE)
        if img is None: continue
        e = cv2.Canny(img, 60, 160)
        edge_p = out_dir / f"{img_p.stem}_edge.png"
        cv2.imwrite(str(edge_p), e)
        pairs.append(Pair(img_p, edge_p))
    return pairs