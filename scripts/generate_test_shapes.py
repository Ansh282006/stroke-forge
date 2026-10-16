"""Generate sample images for the pipeline."""
from __future__ import annotations
from pathlib import Path
import cv2
import numpy as np

OUT = Path("data/samples")
OUT.mkdir(parents=True, exist_ok=True)

def face():
    img = np.zeros((512, 512, 3), dtype=np.uint8)
    cv2.circle(img, (256, 256), 180, (255, 255, 255), 2)
    cv2.circle(img, (196, 220), 18, (255, 255, 255), 2)
    cv2.circle(img, (316, 220), 18, (255, 255, 255), 2)
    cv2.ellipse(img, (256, 320), (70, 40), 0, 0, 180, (255, 255, 255), 2)
    cv2.imwrite(str(OUT / "face.png"), img)

def star():
    img = np.zeros((512, 512, 3), dtype=np.uint8)
    pts = []
    import math
    for i in range(10):
        r = 200 if i % 2 == 0 else 90
        a = -math.pi / 2 + i * math.pi / 5
        pts.append([int(256 + r * math.cos(a)), int(256 + r * math.sin(a))])
    cv2.polylines(img, [np.array(pts)], True, (255, 255, 255), 2)
    cv2.imwrite(str(OUT / "star.png"), img)

if __name__ == "__main__":
    face(); star()
    print(f"wrote samples to {OUT.resolve()}")