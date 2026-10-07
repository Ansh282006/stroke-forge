"""Visualization helpers. Saves a grid of all pipeline stages."""
from __future__ import annotations

from pathlib import Path

import cv2
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from .pipeline import PreprocessResult  # noqa: E402


def plot_stages(
    result: PreprocessResult, output_path: Path, title: str = ""
) -> None:
    panels = [
        ("Original", result.original, True),
        ("Grayscale", result.grayscale, False),
        ("Denoised", result.denoised, False),
        ("CLAHE enhanced", result.enhanced, False),
        ("Otsu threshold", result.otsu, False),
        ("Adaptive threshold", result.adaptive, False),
        ("Canny edges", result.canny, False),
        ("Closed edges", result.closed_edges, False),
        ("Skeleton", result.skeleton, False),
        ("Contour overlay", result.contour_overlay, True),
    ]

    cols = 4
    rows = (len(panels) + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(4 * cols, 3 * rows))
    axes = axes.flatten()

    for ax, (label, img, is_color) in zip(axes, panels):
        if is_color:
            ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        else:
            ax.imshow(img, cmap="gray", vmin=0, vmax=255)
        ax.set_title(label, fontsize=10)
        ax.axis("off")

    for ax in axes[len(panels):]:
        ax.axis("off")

    if title:
        fig.suptitle(title, fontsize=13)

    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=120, bbox_inches="tight")
    plt.close(fig)
