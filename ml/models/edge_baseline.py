"""Tiny U-Net stub (M9).

Kept intentionally minimal: the interface is what matters for M9-M11
to plug in. Real training code goes in ml/train_edge.py.
"""
from __future__ import annotations
try:
    import torch
    import torch.nn as nn
except Exception:  # torch optional at import time
    torch = None
    nn = None

if torch is not None:
    class TinyUNet(nn.Module):
        def __init__(self):
            super().__init__()
            self.enc1 = nn.Conv2d(1, 16, 3, padding=1)
            self.enc2 = nn.Conv2d(16, 32, 3, padding=1)
            self.dec2 = nn.Conv2d(32, 16, 3, padding=1)
            self.dec1 = nn.Conv2d(16, 1, 1)
            self.pool = nn.MaxPool2d(2)
            self.up = nn.Upsample(scale_factor=2, mode="bilinear", align_corners=False)
            self.act = nn.ReLU(inplace=True)
            self.sig = nn.Sigmoid()

        def forward(self, x):
            e1 = self.act(self.enc1(x))
            e2 = self.act(self.enc2(self.pool(e1)))
            d2 = self.act(self.dec2(self.up(e2)))
            return self.sig(self.dec1(d1_skip(d2, e1)))

    def d1_skip(d2, e1):
        return d2 + e1

def build_model():
    if torch is None:
        raise RuntimeError("torch not installed; pip install -r requirements-ml.txt")
    return TinyUNet()