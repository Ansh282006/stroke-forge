# StrokeForge

AI-powered Image-to-Animated Web Code Generator.

Status: Milestone 1 — preprocessing pipeline.

## Setup

    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    python -m pip install -r requirements.txt

## Run

    python scripts\generate_test_shapes.py
    python -m preprocessing.cli --input data\samples\face.png --output data\outputs --verbose
    python -m pytest tests -v
