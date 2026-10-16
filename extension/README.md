# StrokeForge Chrome Extension (M8)

Load unpacked:
1. Open `chrome://extensions`
2. Enable Developer mode
3. "Load unpacked" -> select this folder
4. Start the backend: `python -m backend.cli`
5. Click the StrokeForge icon on any tab, pick a style, preview.

Security model:
- `sandbox.html` is declared with `allow-scripts` only, NOT
  `allow-same-origin`.  The generated page cannot reach extension APIs.
- No remote scripts are loaded by the extension itself.
- `host_permissions` are limited to the local backend.