"""Stage grid visualization (M1)."""
from __future__ import annotations
from pathlib import Path
import cv2
import numpy as np
from .pipeline import PreprocessResult

def save_stage_grid(result: PreprocessResult, out_path) -> Path:
    names = list(result.stages.keys())
    while len(names) < 12: names.append("")
    cols, rows = 4, 3
    h, w = result.canvas["height"], result.canvas["width"]
    tile = 160
    grid = np.zeros((rows * tile, cols * tile, 3), dtype=np.uint8)
    for i, name in enumerate(names[:12]):
        r, c = divmod(i, cols)
        cell = np.zeros((tile, tile, 3), dtype=np.uint8)
        if name:
            img = result.stages[name]
            if img.ndim == 2:
                img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
            img = cv2.resize(img, (tile, tile), interpolation=cv2.INTER_AREA)
            cell = img
            cv2.putText(cell, name, (6, 18), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1, cv2.LINE_AA)
        grid[r*tile:(r+1)*tile, c*tile:(c+1)*tile] = cell
    out_path = Path(out_path); out_path.parent.mkdir(parents=True, exist_ok=True)
    cv2.imwrite(str(out_path), grid)
    return out_path