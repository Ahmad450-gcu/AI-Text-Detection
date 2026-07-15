# VerifyAI Frontend

The frontend for VerifyAI, an app that checks whether a piece of text reads as human written or AI generated. Built with React and Vite, styled with Tailwind CSS.

This app talks to a FastAPI backend that runs the actual model inference. See the backend repo for that side of things.

## Live Demo

https://ai-text-detection-silk.vercel.app/

## Tech Stack

- React 18
- Vite
- Tailwind CSS

## Project Structure

```
Frontend/
├── src/
│   ├── api/
│   │   └── client.js          # handles requests to the backend API
│   ├── components/
│   │   ├── Header.jsx
│   │   ├── Hero.jsx
│   │   ├── AnalyzerCard.jsx    # text input and analyze button
│   │   ├── ResultPanel.jsx     # displays the prediction result
│   │   ├── ConfidenceGauge.jsx # visual confidence indicator
│   │   └── Footer.jsx
│   ├── hooks/
│   │   └── useHealthCheck.js   # checks backend health status
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
├── index.html
├── package.json
├── vite.config.js
├── tailwind.config.js
└── postcss.config.js
```

## Getting Started

### Install dependencies

```bash
npm install
```

### Set up environment variables

```bash
cp .env.example .env
```

Then set the backend URL in `.env`:

```
VITE_API_URL=http://localhost:8000
```

For production, point this at your deployed backend instead, for example:

```
VITE_API_URL=https://your-backend.up.railway.app
```

### Run the dev server

```bash
npm run dev
```

The app will be available at `http://localhost:5173`.

### Build for production

```bash
npm run build
```

This outputs a production ready bundle to the `dist/` folder.

### Preview the production build locally

```bash
npm run preview
```

## Environment Variables

| Variable       | Description                                           |
| -------------- | ----------------------------------------------------- |
| `VITE_API_URL` | Base URL of the backend API the app sends requests to |

Note that Vite bakes environment variables into the build at build time, so if you change `VITE_API_URL` you need to rebuild the app for the change to take effect.

## Deployment

This app deploys cleanly to Vercel with zero extra config.

1. Push this repo to GitHub
2. Import it into Vercel
3. Vercel auto detects the Vite build settings
4. Add `VITE_API_URL` under Environment Variables in the Vercel project settings before deploying
5. Deploy

## Known Limitations

The app depends on the backend being awake and the model being loaded. On a cold start, the first request after backend inactivity can take longer than usual while the model loads into memory, so the analyze button may appear to hang briefly on the very first request.
