"""Typed configuration for the preprocessing pipeline."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml


@dataclass(frozen=True)
class ResizeConfig:
    max_side: int = 1024


@dataclass(frozen=True)
class BilateralConfig:
    d: int = 9
    sigma_color: float = 75.0
    sigma_space: float = 75.0


@dataclass(frozen=True)
class ClaheConfig:
    enabled: bool = True
    clip_limit: float = 2.0
    grid_size: int = 8


@dataclass(frozen=True)
class OtsuConfig:
    invert: bool = True


@dataclass(frozen=True)
class AdaptiveConfig:
    block_size: int = 11
    c: float = 2.0
    invert: bool = True


@dataclass(frozen=True)
class CannyConfig:
    low: int = 50
    high: int = 150
    aperture: int = 3


@dataclass(frozen=True)
class MorphologyConfig:
    kernel_size: int = 3
    iterations: int = 1


@dataclass(frozen=True)
class ContourConfig:
    min_area: float = 20.0


@dataclass(frozen=True)
class PreprocessConfig:
    resize: ResizeConfig = field(default_factory=ResizeConfig)
    bilateral: BilateralConfig = field(default_factory=BilateralConfig)
    clahe: ClaheConfig = field(default_factory=ClaheConfig)
    otsu: OtsuConfig = field(default_factory=OtsuConfig)
    adaptive: AdaptiveConfig = field(default_factory=AdaptiveConfig)
    canny: CannyConfig = field(default_factory=CannyConfig)
    morphology: MorphologyConfig = field(default_factory=MorphologyConfig)
    contours: ContourConfig = field(default_factory=ContourConfig)

    @classmethod
    def from_yaml(cls, path: Path) -> "PreprocessConfig":
        with open(path, "r", encoding="utf-8") as f:
            raw = yaml.safe_load(f) or {}
        return cls(
            resize=ResizeConfig(**raw.get("resize", {})),
            bilateral=BilateralConfig(**raw.get("bilateral", {})),
            clahe=ClaheConfig(**raw.get("clahe", {})),
            otsu=OtsuConfig(**raw.get("otsu", {})),
            adaptive=AdaptiveConfig(**raw.get("adaptive", {})),
            canny=CannyConfig(**raw.get("canny", {})),
            morphology=MorphologyConfig(**raw.get("morphology", {})),
            contours=ContourConfig(**raw.get("contours", {})),
        )
