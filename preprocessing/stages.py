"""Individual preprocessing stages. Each function is pure."""
from __future__ import annotations

import cv2
import numpy as np
from skimage.morphology import skeletonize


def resize_max(image: np.ndarray, max_side: int) -> np.ndarray:
    h, w = image.shape[:2]
    longest = max(h, w)
    if longest <= max_side:
        return image
    scale = max_side / float(longest)
    new_size = (int(round(w * scale)), int(round(h * scale)))
    return cv2.resize(image, new_size, interpolation=cv2.INTER_AREA)


def to_grayscale(image: np.ndarray) -> np.ndarray:
    if image.ndim == 2:
        return image
    if image.shape[2] == 4:
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


def denoise_bilateral(
    gray: np.ndarray, d: int, sigma_color: float, sigma_space: float
) -> np.ndarray:
    return cv2.bilateralFilter(gray, d, sigma_color, sigma_space)


def apply_clahe(gray: np.ndarray, clip_limit: float, grid_size: int) -> np.ndarray:
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(grid_size, grid_size))
    return clahe.apply(gray)


def otsu_threshold(gray: np.ndarray, invert: bool = True) -> np.ndarray:
    _, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return cv2.bitwise_not(th) if invert else th


def adaptive_threshold(
    gray: np.ndarray, block: int, c: float, invert: bool = True
) -> np.ndarray:
    th = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, block, c
    )
    return cv2.bitwise_not(th) if invert else th


def canny_edges(gray: np.ndarray, low: int, high: int, aperture: int) -> np.ndarray:
    return cv2.Canny(gray, low, high, apertureSize=aperture, L2gradient=True)


def morphological_close(binary: np.ndarray, kernel_size: int, iterations: int) -> np.ndarray:
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
    return cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel, iterations=iterations)


def skeletonize_binary(binary: np.ndarray) -> np.ndarray:
    if binary.dtype != np.uint8:
        binary = binary.astype(np.uint8)
    skel = skeletonize(binary > 0)
    return (skel.astype(np.uint8)) * 255


def find_contours(
    binary: np.ndarray, min_area: float
) -> tuple[list[np.ndarray], np.ndarray | None]:
    contours, hierarchy = cv2.findContours(
        binary, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE
    )
    filtered = [c for c in contours if cv2.contourArea(c) >= min_area]
    return filtered, hierarchy
