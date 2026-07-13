# AI Text Detector — Backend API

FastAPI service that serves predictions from a fine-tuned **RoBERTa**
sequence-classification model (Human-written vs. AI-generated text), trained
in `NLP.ipynb` on the HC3 dataset.

## What was verified before this project was built

Rather than trust assumptions, the actual uploaded artifacts and notebook were inspected directly:

| Item | Verified value | How |
|---|---|---|
| Tokenizer loads from just `tokenizer.json` + `tokenizer_config.json` | ✅ Yes, no `vocab.json`/`merges.txt`/`special_tokens_map.json` needed | Loaded `tokenizer.json` directly with the `tokenizers` library and successfully encoded text |
| `MAX_LENGTH` | `256` | Notebook's RoBERTa tokenization cell: `MAX_LEN = 256` |
| Label mapping | `{0: "Human", 1: "AI"}` | `best_model/config.json` → `id2label` / `label2id` (the notebook's own `classification_report` used `target_names=["human","chatgpt"]` for the same 0/1 order) |
| Preprocessing | `normalize_text()` + `clean_text()` (NFKC normalize → strip control chars → collapse whitespace → replace `URL_\d+` with `<URL>`) | Copied directly from the "PREPROCESSING" section of the notebook |
| Lowercasing | RoBERTa input is **NOT** lowercased | Notebook only lowercases for the separate TF-IDF/Logistic-Regression branch (`text_lr`), tokenizing RoBERTa on `answer_text_clean` as-is |
| Custom decision threshold | None — plain `argmax` is used | No threshold search (e.g. `0.63`) found anywhere in the notebook |
| `model.save_pretrained(...)` / `tokenizer.save_pretrained(...)` | Not present in the final notebook cells | The artifacts were exported by a step not shown in the notebook you uploaded — this doesn't matter since the exported files themselves are complete and load correctly |

One extra detail worth knowing: the shipped `tokenizer.json` actually has
padding/truncation to length 256 baked into the file itself. `tokenizer_service.py`
still passes `max_length=256` explicitly rather than relying on that, since
implicit state inside a tokenizer file is fragile.

## Project structure

```
ai-text-detector-backend/
├── app/
│   ├── main.py                  # FastAPI app entrypoint (creation + wiring only)
│   ├── api/
│   │   ├── router.py            # Aggregates endpoint routers
│   │   └── endpoints/
│   │       ├── predict.py       # POST /api/v1/predict
│   │       └── health.py        # GET  /api/v1/health
│   ├── core/
│   │   ├── config.py            # Settings (env vars, paths, device, CORS)
│   │   ├── constants.py         # MAX_LENGTH, ID2LABEL, LABEL2ID
│   │   └── logging.py           # Logging setup
│   ├── models/
│   │   ├── request_models.py    # PredictionRequest
│   │   └── response_models.py   # PredictionResponse, HealthResponse, ErrorResponse
│   ├── services/
│   │   ├── preprocessing.py     # normalize_text(), clean_text()
│   │   ├── tokenizer_service.py # Tokenization only
│   │   ├── model_loader.py      # Loads model/tokenizer once, exposes singletons
│   │   └── prediction_service.py# Orchestrates the full predict pipeline
│   ├── artifacts/
│   │   ├── best_model/          # config.json, model.safetensors, training_args.bin
│   │   ├── tokenizer/           # tokenizer.json, tokenizer_config.json
│   │   └── model_name.json
│   └── utils/
│       └── helpers.py
├── tests/
│   ├── test_health.py
│   ├── test_prediction.py
│   └── test_preprocessing.py
├── requirements.txt
├── Dockerfile
├── .dockerignore
├── .gitignore
├── .env
└── README.md
```

Request flow:

```
Client
  -> POST /api/v1/predict
  -> Pydantic request validation (PredictionRequest)
  -> prediction_service.predict()
       -> preprocessing.clean_text()
       -> tokenizer_service.tokenize()
       -> model forward pass (model_loader.get_model())
       -> softmax -> argmax -> label + confidence
  -> Pydantic response validation (PredictionResponse)
  -> JSON response
```

## Running locally

```bash
cd ai-text-detector-backend
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

pip install -r requirements.txt

uvicorn app.main:app --reload --port 8000
```

Then open http://localhost:8000/docs for interactive Swagger UI.

### Example request

```bash
curl -X POST http://localhost:8000/api/v1/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "The mitochondria is the powerhouse of the cell."}'
```

```json
{
  "prediction": "Human",
  "confidence": 0.87,
  "label_id": 0,
  "probabilities": {"Human": 0.87, "AI": 0.13},
  "processing_time_ms": 42.1
}
```

### Health check

```bash
curl http://localhost:8000/api/v1/health
```

## Running tests

```bash
pytest -v
```

`test_preprocessing.py` is fast (no model loading). `test_health.py` and
`test_prediction.py` load the real model via FastAPI's lifespan handler, so
the first test in each run will take a few seconds.

## Docker

```bash
docker build -t ai-text-detector-backend .
docker run -p 8000:8000 ai-text-detector-backend
```

This bakes the model weights (~500MB) directly into the image. If you'd
rather keep the image slim and mount the weights at deploy time instead,
remove `app/artifacts` from the image and mount it as a volume:

```bash
docker run -p 8000:8000 -v $(pwd)/app/artifacts:/code/app/artifacts ai-text-detector-backend
```

## Deployment notes

- **Frontend (React) on Vercel**: fine, no changes needed.
- **This FastAPI backend on Vercel**: not recommended. A ~500MB transformer
  model needs a long-lived process with the weights loaded in memory —
  Vercel's serverless functions have deployment size, cold-start, and
  execution-time constraints that make this impractical.
- A more common split:
  - Frontend → Vercel
  - Backend (this repo) → Railway, Render, Fly.io, or a VPS
  - Model is loaded once at process startup (already handled by the
    `lifespan` hook in `app/main.py`)

## Environment variables (`.env`)

| Variable | Default | Purpose |
|---|---|---|
| `DEVICE` | `cpu` | Set to `cuda` if deploying with a GPU |
| `LOG_LEVEL` | `INFO` | Standard Python logging levels |

## Extending this project

- Add auth (API key / OAuth) in `app/api/endpoints/predict.py` via a FastAPI dependency.
- Add rate limiting (e.g. `slowapi`) as middleware in `main.py`.
- Add request/response logging or metrics (Prometheus) in `core/logging.py`.
- If you retrain the model, only `app/artifacts/` and, if the label set
  changes, `app/core/constants.py` need to change — nothing else in the
  service layer depends on the specific model.
