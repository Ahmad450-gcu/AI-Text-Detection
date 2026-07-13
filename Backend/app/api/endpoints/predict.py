import logging
from fastapi import APIRouter, HTTPException
from app.models.request_models import PredictionRequest
from app.models.response_models import ErrorResponse, PredictionResponse
from app.services import prediction_service
from app.services.model_loader import is_ready

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/predict",
    response_model=PredictionResponse,
    responses={
        503: {"model": ErrorResponse, "description": "Model not loaded yet"},
        500: {"model": ErrorResponse, "description": "Inference error"},
    },
    summary="Classify text as Human-written or AI-generated",
)
async def predict(request: PredictionRequest) -> PredictionResponse:
    if not is_ready():
        raise HTTPException(
            status_code=503,
            detail="Model is still loading. Please retry in a few seconds.",
        )

    try:
        return prediction_service.predict(request.text)
    except Exception as exc:  # noqa: BLE001 - convert any failure into a clean 500
        logger.exception("Prediction failed for input of length %d", len(request.text))
        raise HTTPException(
            status_code=500,
            detail="Internal error while generating prediction.",
        ) from exc
