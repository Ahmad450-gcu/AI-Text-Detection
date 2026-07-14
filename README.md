# VerifyAI

VerifyAI is a full stack web app that classifies text as human written or AI generated, using a fine tuned RoBERTa model.

Paste any text into the app and it returns a prediction along with a confidence score.

## Live Demo

- Frontend: https://ai-text-detection-silk.vercel.app/
- Backend API docs: `https://ai-text-detection-production.up.railway.app/docs`

## Architecture

```
┌──────────────┐        HTTPS        ┌──────────────────┐        model load        ┌────────────────────┐
│   Frontend   │ ───────────────────▶│      Backend      │◀────────────────────────│   Hugging Face Hub  │
│ React + Vite │                     │      FastAPI       │   transformers library   │ fine tuned RoBERTa  │
│   (Vercel)   │◀─────────────────── │     (Railway)      │                          │  ai-text-detector   │
└──────────────┘   JSON response     └──────────────────┘                          └────────────────────┘
```

The backend does not call an external inference API at request time. The model is downloaded once from the Hugging Face Hub and loaded directly into memory using the `transformers` library when the container starts, then reused for every request.

## Tech Stack

**Frontend**
- React 18
- Vite
- Tailwind CSS
- Deployed on Vercel

**Backend**
- FastAPI
- PyTorch and Hugging Face `transformers`
- Pydantic for request and response validation
- Containerized with Docker, image pushed to Docker Hub
- Deployed on Railway

**Model**
- Fine tuned RoBERTa for sequence classification
- Hosted on the Hugging Face Hub

## Project Structure

```
.
├── Backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── endpoints/
│   │   │   │   ├── health.py
│   │   │   │   └── predict.py
│   │   │   └── router.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── constants.py
│   │   │   └── logging.py
│   │   ├── models/
│   │   │   ├── request_models.py
│   │   │   └── response_models.py
│   │   ├── services/
│   │   │   ├── model_loader.py
│   │   │   ├── prediction_service.py
│   │   │   ├── preprocessing.py
│   │   │   └── tokenizer_service.py
│   │   └── main.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
│
└── Frontend/
    ├── src/
    │   ├── api/client.js
    │   ├── components/
    │   ├── hooks/useHealthCheck.js
    │   ├── App.jsx
    │   └── main.jsx
    ├── package.json
    ├── vite.config.js
    └── .env.example
```

## Getting Started Locally

### Backend

```bash
cd Backend
python -m venv venv
source venv/bin/activate   # on Windows: venv\Scripts\activate
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt
cp .env.example .env
```

Fill in `.env` with your own values:

```
DEVICE=cpu
LOG_LEVEL=INFO
HF_MODEL_ID=your-username/your-model-repo
HF_API_TOKEN=your_hugging_face_token
```

Run the server:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`, with interactive docs at `http://localhost:8000/docs`.

### Frontend

```bash
cd Frontend
npm install
cp .env.example .env
```

Set the backend URL in `.env`:

```
VITE_API_URL=http://localhost:8000
```

Run the dev server:

```bash
npm run dev
```

## Running with Docker

```bash
cd Backend
docker build -t verifyai-backend .
docker run -p 8000:8000 --env-file .env verifyai-backend
```

## API Reference

### `POST /api/v1/predict`

Request body:

```json
{
  "text": "The text you want to classify."
}
```

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

## Environment Variables

**Backend**

| Variable | Description |
|---|---|
| `HF_MODEL_ID` | Hugging Face repo id of the fine tuned model, e.g. `username/ai-text-detector` |
| `HF_API_TOKEN` | Hugging Face access token with read access to the model repo |
| `DEVICE` | `cpu` or `cuda`, depending on the deployment target |
| `LOG_LEVEL` | Logging verbosity, e.g. `INFO` |

**Frontend**

| Variable | Description |
|---|---|
| `VITE_API_URL` | Base URL of the deployed backend, e.g. `https://your-backend.up.railway.app` |

## Known Limitations

Inference latency can range from a couple of seconds up to thirty or more seconds per request. This is mainly because:

- The backend runs on a CPU only instance with no GPU acceleration
- On a cold start, the container has to load roughly five hundred megabytes of model weights into memory before it can serve any request
- PyTorch also needs a brief warm up period to allocate its internal buffers efficiently

This is an active area for improvement, with options such as moving to a GPU backed hosting tier, caching a warm instance, or exploring quantization to reduce inference time.

## Roadmap

- Reduce inference latency
- Add request rate limiting
- Add automated tests for the prediction pipeline
- Add support for batch text analysis


