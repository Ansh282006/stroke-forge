"""Pure stage functions (M1)."""
from __future__ import annotations
from typing import List
import cv2
import numpy as np
from skimage.morphology import skeletonize as sk_skel

from .config import PreprocessConfig

def resize(img, cfg: PreprocessConfig):
    w, h = cfg.resize.width, cfg.resize.height
    if cfg.resize.keep_aspect:
        ih, iw = img.shape[:2]
        s = min(w / iw, h / ih)
        nw, nh = max(1, int(iw * s)), max(1, int(ih * s))
        img = cv2.resize(img, (nw, nh), interpolation=cv2.INTER_AREA)
        canvas = np.zeros((h, w, 3), dtype=img.dtype) if img.ndim == 3 else np.zeros((h, w), dtype=img.dtype)
        oy, ox = (h - nh) // 2, (w - nw) // 2
        if img.ndim == 3: canvas[oy:oy+nh, ox:ox+nw] = img
        else: canvas[oy:oy+nh, ox:ox+nw] = img
        return canvas
    return cv2.resize(img, (w, h), interpolation=cv2.INTER_AREA)

def to_gray(img):
    if img.ndim == 2: return img
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def denoise(gray, cfg):
    if cfg.denoise.method == "bilateral":
        return cv2.bilateralFilter(gray, cfg.denoise.d, cfg.denoise.sigma_color, cfg.denoise.sigma_space)
    if cfg.denoise.method == "gaussian":
        return cv2.GaussianBlur(gray, (5, 5), 0)
    if cfg.denoise.method == "median":
        return cv2.medianBlur(gray, 5)
    return gray

def contrast(gray, cfg):
    if cfg.contrast.method == "clahe":
        clahe = cv2.createCLAHE(clipLimit=cfg.contrast.clip_limit, tileGridSize=tuple(cfg.contrast.tile_grid))
        return clahe.apply(gray)
    if cfg.contrast.method == "equalize":
        return cv2.equalizeHist(gray)
    return gray

def threshold(gray, cfg):
    if cfg.threshold.method == "otsu":
        _, b = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        return b
    if cfg.threshold.method == "adaptive":
        return cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    return gray

def edges(gray, cfg):
    if cfg.edges.method == "canny":
        return cv2.Canny(gray, cfg.edges.low, cfg.edges.high)
    if cfg.edges.method == "sobel":
        gx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        gy = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        mag = np.hypot(gx, gy)
        return np.clip(mag, 0, 255).astype(np.uint8)
    if cfg.edges.method == "laplacian":
        lap = cv2.Laplacian(gray, cv2.CV_64F)
        return np.clip(np.abs(lap), 0, 255).astype(np.uint8)
    return gray

def morphology_close(binary, cfg):
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (cfg.morphology.close_kernel,) * 2)
    return cv2.morphologyEx(binary, cv2.MORPH_CLOSE, k, iterations=cfg.morphology.close_iter)

def skeletonize(binary, cfg):
    if not cfg.skeleton.enabled: return binary
    b = binary.astype(bool)
    sk = sk_skel(b)
    return (sk.astype(np.uint8)) * 255

def find_contours(binary):
    cts, _ = cv2.findContours(binary, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    return list(cts)