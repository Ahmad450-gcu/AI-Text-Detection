# VerifyAI Backend

The backend for VerifyAI, an app that checks whether a piece of text reads as human written or AI generated. Built with FastAPI, serving a fine tuned RoBERTa model for text classification.

The model is downloaded from the Hugging Face Hub and loaded directly into memory using the `transformers` library when the app starts. There is no dependency on an external inference API at request time.

## Tech Stack

- FastAPI
- PyTorch and Hugging Face `transformers`
- Pydantic for request and response validation
- Docker for containerization
- Deployed on Railway

## Project Structure

```
Backend/
├── app/
│   ├── api/
│   │   ├── endpoints/
│   │   │   ├── health.py       # health check route
│   │   │   └── predict.py      # prediction route
│   │   └── router.py           # combines all routes
│   ├── core/
│   │   ├── config.py           # environment based settings
│   │   ├── constants.py        # label mapping and thresholds
│   │   └── logging.py          # logging setup
│   ├── models/
│   │   ├── request_models.py   # request schema
│   │   └── response_models.py  # response schema
│   ├── services/
│   │   ├── model_loader.py     # loads model and tokenizer from Hugging Face Hub
│   │   ├── prediction_service.py  # runs inference
│   │   ├── preprocessing.py    # text cleaning
│   │   └── tokenizer_service.py   # tokenization logic
│   ├── utils/
│   │   └── helpers.py
│   └── main.py                 # app entrypoint
├── tests/
├── Dockerfile
├── requirements.txt
└── .env.example
```

## Getting Started

### Set up a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # on Windows: venv\Scripts\activate
```

### Install dependencies

PyTorch is installed separately first to make sure the CPU only build is used, keeping the install lighter:

```bash
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
```

### Set up environment variables

```bash
cp .env.example .env
```

Fill in `.env` with your own values:

```
DEVICE=cpu
LOG_LEVEL=INFO
HF_MODEL_ID=your-username/your-model-repo
HF_API_TOKEN=your_hugging_face_token
```

`HF_API_TOKEN` needs at least read access to the model repo. Generate one at huggingface.co under Settings, Access Tokens.

### Run the server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`, with interactive docs at `http://localhost:8000/docs`.

## Running with Docker

```bash
docker build -t verifyai-backend .
docker run -p 8000:8000 --env-file .env verifyai-backend
```

## API Reference

### `GET /`

Basic root route confirming the service is running, with links to docs and the health check.

### `GET /api/v1/health`

Returns whether the model has finished loading.

```json
{
    "status": "ok",
    "model_loaded": true,
    "model_name": "RoBERTa",
    "device": "cpu"
}
```

### `POST /api/v1/predict`

Request body:

```json
{
    "text": "The text you want to classify."
}
```

`text` must be non empty, non whitespace only, and no longer than 10,000 characters.

Response:

```json
{
    "prediction": "Human",
    "confidence": 0.93,
    "label_id": 0,
    "probabilities": {
        "Human": 0.93,
        "AI": 0.07
    },
    "processing_time_ms": 812.4
}
```

## Environment Variables

| Variable       | Description                                                                    |
| -------------- | ------------------------------------------------------------------------------ |
| `HF_MODEL_ID`  | Hugging Face repo id of the fine tuned model, e.g. `username/ai-text-detector` |
| `HF_API_TOKEN` | Hugging Face access token with read access to the model repo                   |
| `DEVICE`       | `cpu` or `cuda`, depending on the deployment target                            |
| `LOG_LEVEL`    | Logging verbosity, e.g. `INFO`                                                 |

## Running Tests

```bash
pytest
```

## Deployment

This backend is built as a Docker image and deployed on Railway.

1. Push the image to a container registry, or connect the repo directly to Railway for automatic builds
2. Set `HF_MODEL_ID` and `HF_API_TOKEN` under the Variables tab in the Railway service
3. Deploy

On first startup after a deploy, the container downloads the model from the Hugging Face Hub before it can serve requests, so the first health check or prediction may take longer than usual.

## Known Limitations

Inference runs on CPU only, with no GPU acceleration. This means:

- Cold starts are slow, since roughly five hundred megabytes of model weights need to load into memory
- PyTorch needs a brief warm up period before inference runs at normal speed
- Response times can range from a couple of seconds to significantly longer depending on load and whether the instance has just started
