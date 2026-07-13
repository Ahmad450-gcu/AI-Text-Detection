from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# app/core/config.py -> parents[1] = app/
APP_DIR = Path(__file__).resolve().parents[1]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- General app metadata ---
    APP_NAME: str = "AI Text Detector API"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = (
        "Serves predictions from a fine-tuned RoBERTa model that classifies "
        "text as Human-written or AI-generated."
    )
    API_PREFIX: str = "/api/v1"

    # --- Artifact locations (relative to app/) ---
    ARTIFACTS_DIR: Path = APP_DIR / "artifacts"
    MODEL_DIR: Path = ARTIFACTS_DIR / "best_model"
    TOKENIZER_DIR: Path = ARTIFACTS_DIR / "tokenizer"
    MODEL_NAME_FILE: Path = ARTIFACTS_DIR / "model_name.json"

    # Human-friendly name, falls back to this if model_name.json can't be read
    MODEL_DISPLAY_NAME: str = "RoBERTa"

    # --- Inference ---
    # "cpu" by default. Set DEVICE=cuda in .env if deploying with a GPU.
    DEVICE: str = "cpu"

    # --- Logging ---
    LOG_LEVEL: str = "INFO"

    # --- CORS ---
    # Tighten this to your actual frontend origin(s) before going to production,
    # e.g. ["https://your-frontend.vercel.app"]
    CORS_ORIGINS: list[str] = ["*"]


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance — Settings() is only ever constructed once."""
    return Settings()


settings = get_settings()
