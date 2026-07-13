# VerifyAI — React Frontend

A React (Vite + Tailwind) frontend for the AI Text Detector API, based on the
design you shared, adapted to what the backend can actually support today.

## What's different from the design, and why

| In the design | In this build | Why |
|---|---|---|
| Upload a file | Not included | The backend's `/predict` endpoint only accepts a JSON `{"text": "..."}` body — no file upload, no `.txt`/`.docx`/`.pdf` parsing exists yet. Per your call, this was left out rather than built as a non-functional button. |
| A "detailed explanation" panel with highlighted phrases in the analyzed text | A probability breakdown (Human % vs AI %) instead | The model returns a label + confidence + per-class probabilities — nothing about *which words* drove the decision. Building a fake-looking explanation would misrepresent what the model actually knows. If you want real highlighting later, that needs a token-attribution method (e.g. attention weights or SHAP) added to the backend — happy to help with that as a separate step. |
| Exact colors/type | A distinct palette (see below) | The source image was only 69×339px — too small to read exact hex values or copy, so I made deliberate design choices in the same spirit (minimal, light background, black CTA, single-column card layout) rather than guessing at pixels that weren't really visible. |

## Design decisions

- **Type**: Space Grotesk (display/headings) + IBM Plex Sans (body) + IBM Plex Mono (numbers — confidence %, char count, timing). Loaded via Google Fonts in `index.html`.
- **Color**: `ink` #14171A (text), `surface` #F4F5F2 (result card bg), `verified` #2F5D50 (Human result state), `flagged` #B5502F (AI result state).
- **Signature element**: the confidence gauge is a hand-built SVG dial with tick marks, like a measurement instrument — a nod to "verification" as literally taking a reading, not just a plain progress ring.
- Built mobile-first / single centered column (matches the narrow layout in your screenshot), capped at `max-w-app` (560px) so it stays readable on desktop too.

## Project structure

```
verifyai-frontend/
├── index.html
├── package.json
├── vite.config.js
├── tailwind.config.js
├── postcss.config.js
├── .env.example              # VITE_API_URL
└── src/
    ├── main.jsx
    ├── App.jsx
    ├── index.css
    ├── api/
    │   └── client.js         # fetch wrapper: checkHealth(), predictText()
    ├── hooks/
    │   └── useHealthCheck.js # pings /health on mount for the status dot
    └── components/
        ├── Header.jsx        # brand mark + live backend status dot
        ├── Hero.jsx           # title + subtitle
        ├── AnalyzerCard.jsx  # textarea + char count + Analyze button
        ├── ConfidenceGauge.jsx  # the SVG dial
        ├── ResultPanel.jsx   # gauge + probability bars + timing
        └── Footer.jsx        # disclaimer
```

## Running it locally

**1. Start the backend first** (see the backend project's own README):

```bash
uvicorn app.main:app --port 8000
```

**2. Configure the API URL:**

```bash
cp .env.example .env
# .env now contains: VITE_API_URL=http://localhost:8000
```

**3. Install and run:**

```bash
npm install
npm run dev
```

Open **http://localhost:5173**.

## What was actually verified before this was handed to you

- `npm install` and `npm run build` were run for real — this isn't just
  code that looks right, it compiles cleanly with no errors.
- The exact request/response handling logic in `src/api/client.js` (status
  code branching for 200 / 422 / 503 / network failure) was tested against
  the real, running FastAPI backend — including a real prediction, an empty
  string, and a whitespace-only string — and every case produced the
  expected message.
- I don't have a browser available in the environment I built this in, so I
  could not take a screenshot to visually check it against your design.
  Run `npm run dev` and take a look — if anything's visually off, send me
  a screenshot or describe what to change and I'll adjust it.

## Deploying

This is a static Vite app — deploys to Vercel/Netlify/Cloudflare Pages as-is:

```bash
npm run build   # outputs to dist/
```

Set `VITE_API_URL` as an environment variable on your hosting platform to
point at your deployed backend (e.g. Railway/Render/Fly.io URL) instead of
`localhost`.
