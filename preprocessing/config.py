"""YAML-driven config dataclasses (M1)."""
from __future__ import annotations
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Tuple
import yaml

@dataclass
class ResizeCfg:
    width: int = 512
    height: int = 512
    keep_aspect: bool = True

@dataclass
class DenoiseCfg:
    method: str = "bilateral"
    d: int = 9
    sigma_color: int = 75
    sigma_space: int = 75

@dataclass
class ContrastCfg:
    method: str = "clahe"
    clip_limit: float = 2.0
    tile_grid: Tuple[int, int] = (8, 8)

@dataclass
class ThresholdCfg:
    method: str = "otsu"

@dataclass
class EdgesCfg:
    method: str = "canny"
    low: int = 60
    high: int = 160

@dataclass
class MorphCfg:
    close_kernel: int = 3
    close_iter: int = 1

@dataclass
class SkeletonCfg:
    enabled: bool = True

@dataclass
class ContoursCfg:
    mode: str = "RETR_LIST"
    method: str = "CHAIN_APPROX_SIMPLE"
    min_area: float = 25.0

@dataclass
class PreprocessConfig:
    resize: ResizeCfg = field(default_factory=ResizeCfg)
    grayscale: Dict[str, Any] = field(default_factory=lambda: {"enabled": True})
    denoise: DenoiseCfg = field(default_factory=DenoiseCfg)
    contrast: ContrastCfg = field(default_factory=ContrastCfg)
    threshold: ThresholdCfg = field(default_factory=ThresholdCfg)
    edges: EdgesCfg = field(default_factory=EdgesCfg)
    morphology: MorphCfg = field(default_factory=MorphCfg)
    skeleton: SkeletonCfg = field(default_factory=SkeletonCfg)
    contours: ContoursCfg = field(default_factory=ContoursCfg)

def _as(cls, data):
    if data is None: return cls()
    if isinstance(data, cls): return data
    return cls(**data)

def load_config(path) -> PreprocessConfig:
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    return PreprocessConfig(
        resize=_as(ResizeCfg, raw.get("resize")),
        grayscale=raw.get("grayscale", {"enabled": True}),
        denoise=_as(DenoiseCfg, raw.get("denoise")),
        contrast=_as(ContrastCfg, raw.get("contrast")),
        threshold=_as(ThresholdCfg, raw.get("threshold")),
        edges=_as(EdgesCfg, raw.get("edges")),
        morphology=_as(MorphCfg, raw.get("morphology")),
        skeleton=_as(SkeletonCfg, raw.get("skeleton")),
        contours=_as(ContoursCfg, raw.get("contours")),
    )

def default_config() -> PreprocessConfig:
    return PreprocessConfig()