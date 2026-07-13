import logging
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from app.core.config import settings

logger = logging.getLogger(__name__)

_model = None
_tokenizer = None
_ready = False


def load_artifacts(force_reload: bool = False) -> None:
    global _model, _tokenizer, _ready

    if _ready and not force_reload:
        return

    logger.info("Loading model '%s' from Hugging Face Hub...", settings.HF_MODEL_ID)
    token = settings.HF_API_TOKEN or None

    try:
        _tokenizer = AutoTokenizer.from_pretrained(settings.HF_MODEL_ID, token=token)
        _model = AutoModelForSequenceClassification.from_pretrained(
            settings.HF_MODEL_ID, token=token
        )
        _model.to(settings.DEVICE)
        _model.eval()
        _ready = True
        logger.info("Model loaded successfully on device '%s'.", settings.DEVICE)
    except Exception:
        logger.exception("Failed to load model/tokenizer from Hugging Face Hub.")
        _ready = False


def get_model():
    return _model


def get_tokenizer():
    return _tokenizer


def get_device() -> str:
    return settings.DEVICE


def get_model_display_name() -> str:
    return settings.MODEL_DISPLAY_NAME


def is_ready() -> bool:
    return _ready