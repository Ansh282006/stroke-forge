"""Generate simple synthetic test images."""
from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np

OUT_DIR = Path(__file__).resolve().parent.parent / "data" / "samples"
SIZE = 512
WHITE = 255
BLACK = (0, 0, 0)


def _canvas() -> np.ndarray:
    return np.full((SIZE, SIZE, 3), WHITE, dtype=np.uint8)


def circle() -> np.ndarray:
    img = _canvas()
    cv2.circle(img, (256, 256), 160, BLACK, 4)
    return img


def rectangle() -> np.ndarray:
    img = _canvas()
    cv2.rectangle(img, (100, 130), (412, 380), BLACK, 4)
    return img


def triangle() -> np.ndarray:
    img = _canvas()
    pts = np.array([[256, 80], [80, 430], [432, 430]], dtype=np.int32)
    cv2.polylines(img, [pts], isClosed=True, color=BLACK, thickness=4)
    return img


def face() -> np.ndarray:
    img = _canvas()
    cv2.circle(img, (256, 256), 170, BLACK, 4)
    cv2.circle(img, (200, 210), 15, BLACK, 3)
    cv2.circle(img, (312, 210), 15, BLACK, 3)
    cv2.ellipse(img, (256, 320), (70, 40), 0, 0, 180, BLACK, 3)
    return img


def star() -> np.ndarray:
    img = _canvas()
    pts = []
    for i in range(10):
        r = 170 if i % 2 == 0 else 70
        angle = -np.pi / 2 + i * np.pi / 5
        pts.append([int(256 + r * np.cos(angle)), int(256 + r * np.sin(angle))])
    pts_arr = np.array(pts, dtype=np.int32)
    cv2.polylines(img, [pts_arr], isClosed=True, color=BLACK, thickness=4)
    return img


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    shapes = {
        "circle.png": circle(),
        "rectangle.png": rectangle(),
        "triangle.png": triangle(),
        "face.png": face(),
        "star.png": star(),
    }
    for name, img in shapes.items():
        path = OUT_DIR / name
        cv2.imwrite(str(path), img)
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
