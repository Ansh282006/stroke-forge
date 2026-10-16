"""Runs the M1 -> M6 chain in-process (M7)."""
from __future__ import annotations
import json
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

import cv2

from preprocessing.config import default_config
from preprocessing.pipeline import run as run_pre
from vectorization.extractor import contours_to_paths
from vectorization.serializer import save as save_paths
from stroke_engine.orderer import order_paths
from stroke_engine.serializer import save_ordered
from style_engine.styles import get_style
from style_engine.apply import apply_style
from code_generator.options import GeneratorOptions
from code_generator.generator import generate_bundle


@dataclass
class JobResult:
    job_id: str
    job_dir: Path
    bundle_dir: Path
    preview_file: Path
    style: str
    name: str
    total_ms: int
    files: list


def process_image(
    image_bytes: bytes,
    filename: str,
    style_name: str,
    job_root: Path,
    name: str | None = None,
    loop: bool = True,
    speed: float = 1.0,
) -> JobResult:
    job_id = uuid.uuid4().hex[:12]
    job_dir = Path(job_root) / job_id
    job_dir.mkdir(parents=True, exist_ok=True)

    # Persist the upload so preprocessing can read it via cv2.imread
    raw = job_dir / f"input_{Path(filename).name}"
    raw.write_bytes(image_bytes)

    # M1: preprocess
    pre = run_pre(raw, default_config())

    # M2: extract paths
    doc = contours_to_paths(pre.contours, pre.canvas, pre.filename, epsilon=1.2)
    paths_json = job_dir / f"{raw.stem}_paths.json"
    save_paths(doc, paths_json)

    # M3: order
    doc = order_paths(doc)
    ordered_json = job_dir / f"{raw.stem}_ordered.json"
    save_ordered(doc, ordered_json)

    # M4: style
    style = get_style(style_name)
    ordered_doc = json.loads(ordered_json.read_text(encoding="utf-8"))
    styled = apply_style(ordered_doc, style)
    styled_json = job_dir / f"{raw.stem}_{style.name}.json"
    styled_json.write_text(json.dumps(styled.to_dict(), indent=2), encoding="utf-8")

    # M6: bundle
    bundle_name = name or f"{raw.stem}_{style.name}"
    opts = GeneratorOptions(name=bundle_name, title=f"StrokeForge - {bundle_name}",
                            autoplay=True, loop=loop, speed=speed)
    result = generate_bundle(styled.to_dict(), job_dir / "web", opts)

    return JobResult(
        job_id=job_id,
        job_dir=job_dir,
        bundle_dir=result.out_dir,
        preview_file=result.out_dir / "index.html",
        style=style.name,
        name=bundle_name,
        total_ms=result.total_ms,
        files=[f.name for f in result.files],
    )