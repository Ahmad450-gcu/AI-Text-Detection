import time
import torch
import torch.nn.functional as F
from app.core.constants import ID2LABEL
from app.models.response_models import PredictionResponse
from app.services.model_loader import get_device, get_model
from app.services.preprocessing import clean_text
from app.services.tokenizer_service import tokenize

def predict(raw_text: str) -> PredictionResponse:
    start = time.perf_counter()

    cleaned_text = clean_text(raw_text)

    device = get_device()
    model = get_model()

    inputs = tokenize(cleaned_text)
    inputs = {key: tensor.to(device) for key, tensor in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)
        probabilities = F.softmax(outputs.logits, dim=-1).squeeze(0)

    predicted_id = int(torch.argmax(probabilities).item())
    confidence = float(probabilities[predicted_id].item())

    probability_by_label = {
        ID2LABEL[idx]: round(float(prob.item()), 6)
        for idx, prob in enumerate(probabilities)
    }

    elapsed_ms = (time.perf_counter() - start) * 1000

    return PredictionResponse(
        prediction=ID2LABEL[predicted_id],
        confidence=round(confidence, 6),
        label_id=predicted_id,
        probabilities=probability_by_label,
        processing_time_ms=round(elapsed_ms, 2),
    )
