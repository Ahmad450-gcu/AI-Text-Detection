from fastapi import APIRouter
from app.models.response_models import HealthResponse
from app.services.model_loader import get_device, get_model_display_name, is_ready

router = APIRouter()

@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    description="Returns whether the model/tokenizer have finished loading and are ready to serve predictions.",
)
async def health() -> HealthResponse:
    ready = is_ready()
    return HealthResponse(
        status="ok" if ready else "loading",
        model_loaded=ready,
        model_name=get_model_display_name() if ready else "unknown",
        device=str(get_device()) if ready else "unknown",
    )
