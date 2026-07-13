from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


APP_DIR = Path(__file__).resolve().parents[1]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    APP_NAME: str = "AI Text Detector API"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = (
        "Serves predictions from a fine-tuned RoBERTa model that classifies "
        "text as Human-written or AI-generated."
    )
    API_PREFIX: str = "/api/v1"

    ARTIFACTS_DIR: Path = APP_DIR / "artifacts"
    MODEL_DIR: Path = ARTIFACTS_DIR / "best_model"
    TOKENIZER_DIR: Path = ARTIFACTS_DIR / "tokenizer"
    MODEL_NAME_FILE: Path = ARTIFACTS_DIR / "model_name.json"

    MODEL_DISPLAY_NAME: str = "RoBERTa"


    DEVICE: str = "cpu"

    HF_MODEL_ID: str = "dev-Ahmad450/ai-text-detector"

    HF_API_TOKEN: str = ""


    LOG_LEVEL: str = "INFO"


    CORS_ORIGINS: list[str] = ["*"]


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance — Settings() is only ever constructed once."""
    return Settings()


settings = get_settings()
