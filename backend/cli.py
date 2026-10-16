"""Backend CLI (M7)."""
from __future__ import annotations
import argparse, sys
import uvicorn

def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="StrokeForge backend (M7)")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--reload", action="store_true")
    args = ap.parse_args(argv)
    uvicorn.run("backend.app:app", host=args.host, port=args.port, reload=args.reload)
    return 0

if __name__ == "__main__":
    sys.exit(main())