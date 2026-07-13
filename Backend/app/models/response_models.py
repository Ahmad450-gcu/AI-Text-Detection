from pydantic import BaseModel, Field

class PredictionResponse(BaseModel):

    prediction: str = Field(
        ..., description="Predicted class label, e.g. 'Human' or 'AI'."
    )
    confidence: float = Field(
        ..., ge=0.0, le=1.0, description="Softmax probability of the predicted class."
    )
    label_id: int = Field(..., description="Numeric id of the predicted class (0 or 1).")
    probabilities: dict[str, float] = Field(
        ..., description="Softmax probability for every class, keyed by label name."
    )
    processing_time_ms: float = Field(
        ..., description="Time taken to run preprocessing + inference, in milliseconds."
    )


class HealthResponse(BaseModel):

    status: str = Field(..., description="'ok' once the model is loaded, else 'loading'.")
    model_loaded: bool
    model_name: str
    device: str


class ErrorResponse(BaseModel):
    detail: str
