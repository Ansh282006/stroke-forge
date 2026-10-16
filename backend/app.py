"""FastAPI app factory (M7)."""
from __future__ import annotations
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config import get_settings
from backend.routes.health import router as health_router
from backend.routes.generate import router as generate_router
from backend.routes.jobs import router as jobs_router

def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title="StrokeForge API", version="0.7.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(settings.cors_origins) or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(health_router, prefix="/api", tags=["health"])
    app.include_router(generate_router, prefix="/api", tags=["generate"])
    app.include_router(jobs_router, prefix="/api", tags=["jobs"])
    return app

app = create_app()