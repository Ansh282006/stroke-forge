# StrokeForge

AI-powered Image-to-Animated Web Code Generator.

Upload a raster image -> classical CV + ML extract a drawable
representation -> ordered strokes -> styled animation -> executable
HTML/CSS/JS/Tailwind code that runs in the browser and inside a
sandboxed Chrome extension.

## Quick start

    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    python -m pip install --upgrade pip
    python -m pip install -r requirements.txt

    python scripts\generate_test_shapes.py
    python -m preprocessing.cli  --input data\samples\face.png --output data\outputs --verbose
    python -m vectorization.cli  --input data\samples\face.png --output data\outputs --verbose
    python -m stroke_engine.cli  --input data\outputs\face_paths.json --output data\outputs --verbose
    python -m style_engine.cli   --input data\outputs\face_ordered.json --style neon --output data\outputs --verbose
    python -m animation_engine.cli --input data\outputs\face_neon.json --output data\outputs --name face_neon --loop --verbose
    python -m code_generator.cli   --input data\outputs\face_neon.json --output data\outputs\web --name face_neon --loop --verbose

## Backend (M7)

    python -m backend.cli --host 127.0.0.1 --port 8000

## Frontend (M7)

    cd frontend
    npm install
    npm run dev

## Tests

    python -m pytest tests -v

## Roadmap

- M0  Discovery + design                  done
- M1  Preprocessing pipeline              done
- M2  Drawable representation             done
- M3  Stroke ordering + timeline          done
- M4  Style engine + Outline + Neon       done
- M5  Animation engine                    done
- M6  Code generator                      done
- M7  Web app MVP                         done
- M8  Browser extension MVP               done
- M9  ML dataset + baseline               skeleton
- M10 ML edge refinement                  skeleton
- M11 ML stroke ordering                  skeleton
- M12 Extra styles + Tailwind output      done
- M13 Advanced features                   pending
- M14 NLP (future)                        pending