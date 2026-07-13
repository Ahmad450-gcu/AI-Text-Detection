from pydantic import BaseModel, Field, field_validator

class PredictionRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=10_000,
        description="The text to classify as Human-written or AI-generated.",
        examples=["The quick brown fox jumps over the lazy dog."],
    )

    @field_validator("text")
    @classmethod
    def text_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("text must not be empty or whitespace-only")
        return value
