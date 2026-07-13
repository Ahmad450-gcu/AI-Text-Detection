from transformers import BatchEncoding
from app.core.constants import MAX_LENGTH
from app.services.model_loader import get_tokenizer

def tokenize(text: str) -> BatchEncoding:
    tokenizer = get_tokenizer()
    return tokenizer(
        text,
        truncation=True,
        padding="max_length",
        max_length=MAX_LENGTH,
        return_attention_mask=True,
        return_tensors="pt",
    )
