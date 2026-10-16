"""Health route (M7)."""
from fastapi import APIRouter
from backend.schemas import Health

router = APIRouter()

@router.get("/health", response_model=Health)
def health() -> Health:
    return Health()