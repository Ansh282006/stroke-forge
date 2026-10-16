$ErrorActionPreference = "Stop"
Set-Location "C:\Users\anshb\Desktop\Hack\Project\stroke-forge\stroke-forge"
.\.venv\Scripts\Activate.ps1

python scripts\generate_test_shapes.py
python -m preprocessing.cli  --input data\samples\face.png --output data\outputs --verbose
python -m vectorization.cli  --input data\samples\face.png --output data\outputs --verbose
python -m stroke_engine.cli  --input data\outputs\face_paths.json --output data\outputs --verbose
python -m style_engine.cli   --input data\outputs\face_ordered.json --style outline --output data\outputs --verbose
python -m style_engine.cli   --input data\outputs\face_ordered.json --style neon    --output data\outputs --verbose
python -m animation_engine.cli --input data\outputs\face_neon.json --output data\outputs --name face_neon --loop --verbose
python -m code_generator.cli   --input data\outputs\face_neon.json --output data\outputs\web --name face_neon --loop --verbose
Write-Host "`nDone. Open data\outputs\web\face_neon\index.html" -ForegroundColor Green