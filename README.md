# StrokeForge

AI-powered Image-to-Animated Web Code Generator.

Converts a raster image into ordered vector paths and (eventually) into animated HTML/CSS/JS code with selectable visual styles.

## Pipeline

    Image
    -> Preprocessing (OpenCV)
    -> Vectorization (contours -> paths)
    -> Stroke Ordering + Timeline
    -> Style Engine        (M4)
    -> Animation Engine    (M5)
    -> Code Generation     (M6)
    -> Web App             (M7)
    -> Browser Extension   (M8)

## Setup

    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    python -m pip install -r requirements.txt

## Run

    python scripts\generate_test_shapes.py
    python -m preprocessing.cli --input data\samples\face.png --output data\outputs
    python -m vectorization.cli --input data\samples\face.png --output data\outputs
    python -m stroke_engine.cli --input data\outputs\face_paths.json --output data\outputs

## Test

    python -m pytest tests -v

## Status

Milestones 1-3 complete: preprocessing, vectorization, stroke ordering.
