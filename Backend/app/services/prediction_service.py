import time
import logging
import torch
from app.core.constants import ID2LABEL
from app.models.response_models import PredictionResponse
from app.services.model_loader import get_model, get_device
from app.services.preprocessing import clean_text
from app.services.tokenizer_service import tokenize

logger = logging.getLogger(__name__)


def predict(raw_text: str) -> PredictionResponse:
    start = time.perf_counter()
    cleaned_text = clean_text(raw_text)

    try:
        model = get_model()
        device = get_device()

        encoded = tokenize(cleaned_text)
        encoded = {k: v.to(device) for k, v in encoded.items()}

        with torch.no_grad():
            outputs = model(**encoded)
            probs = torch.softmax(outputs.logits, dim=-1).squeeze(0)

        predicted_id = int(torch.argmax(probs).item())
        confidence = float(probs[predicted_id].item())

        probability_by_label = {
            ID2LABEL.get(i, str(i)): round(float(probs[i].item()), 6)
            for i in range(probs.shape[0])
        }
        final_prediction = ID2LABEL.get(predicted_id, str(predicted_id))

    except Exception as exc:
        logger.error("Inference failed: %s", exc)
        return PredictionResponse(
            prediction="Error reaching AI Engine",
            confidence=0.0,
            label_id=0,
            probabilities={},
            processing_time_ms=round((time.perf_counter() - start) * 1000, 2),
        )

    elapsed_ms = (time.perf_counter() - start) * 1000
    return PredictionResponse(
        prediction=final_prediction,
        confidence=round(confidence, 6),
        label_id=predicted_id,
        probabilities=probability_by_label,
        processing_time_ms=round(elapsed_ms, 2),
    )