import json
import logging
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from app.core.config import settings

logger = logging.getLogger(__name__)

_model = None
_tokenizer = None
_device: torch.device | None = None
_model_display_name: str | None = None


def _read_model_display_name() -> str:
    try:
        with open(settings.MODEL_NAME_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("best_model_name", settings.MODEL_DISPLAY_NAME)
    except (FileNotFoundError, json.JSONDecodeError, OSError) as exc:
        logger.warning(
            "Could not read model_name.json (%s), falling back to default display name.",
            exc,
        )
        return settings.MODEL_DISPLAY_NAME


def load_artifacts(force_reload: bool = False) -> None:
    global _model, _tokenizer, _device, _model_display_name

    if not force_reload and _model is not None and _tokenizer is not None:
        logger.info("Model and tokenizer already loaded — skipping reload.")
        return

    _device = torch.device(settings.DEVICE)
    _model_display_name = _read_model_display_name()

    logger.info("Loading tokenizer from %s", settings.TOKENIZER_DIR)
    _tokenizer = AutoTokenizer.from_pretrained(str(settings.TOKENIZER_DIR))

    logger.info("Loading model (%s) from %s", _model_display_name, settings.MODEL_DIR)
    _model = AutoModelForSequenceClassification.from_pretrained(str(settings.MODEL_DIR))
    _model.to(_device)
    _model.eval()

    logger.info("Model and tokenizer loaded successfully on device=%s", _device)


def get_model():
    if _model is None:
        raise RuntimeError(
            "Model has not been loaded yet. Ensure load_artifacts() runs at app startup."
        )
    return _model


def get_tokenizer():
    if _tokenizer is None:
        raise RuntimeError(
            "Tokenizer has not been loaded yet. Ensure load_artifacts() runs at app startup."
        )
    return _tokenizer


def get_device() -> torch.device:
    if _device is None:
        raise RuntimeError(
            "Device has not been set yet. Ensure load_artifacts() runs at app startup."
        )
    return _device


def get_model_display_name() -> str:
    return _model_display_name or settings.MODEL_DISPLAY_NAME


def is_ready() -> bool:
    return _model is not None and _tokenizer is not None
