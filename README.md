# Language Detector

A FastAPI + HTML frontend for language detection using a FastText model.

## Project Structure

```
language-detector/
├── api/
│   ├── index.py              # FastAPI backend
│   ├── requirements.txt      # Python dependencies
│   └── language_detector.bin # ← YOUR MODEL FILE (add this!)
├── frontend/
│   └── index.html            # Frontend UI
├── vercel.json               # Vercel deployment config
└── README.md
```

## Step 1 — Add your model

Copy your trained model into the `api/` folder:

```bash
cp /path/to/language_detector.bin api/language_detector.bin
```

## Step 2 — Run locally

```bash
# Install dependencies
pip install -r api/requirements.txt

# Start the backend
uvicorn api.index:app --reload --port 8000
```

Then open `frontend/index.html` in your browser.

> **Note:** For local development, change the fetch URL in `frontend/index.html` from `/api/detect` to `http://localhost:8000/detect`.

## Step 3 — Deploy to Vercel

### Prerequisites
- [Vercel CLI](https://vercel.com/docs/cli): `npm i -g vercel`
- A Vercel account

### Deploy

```bash
# From the project root
vercel

# Follow the prompts, then deploy to production:
vercel --prod
```

Vercel will automatically:
- Serve the FastAPI backend at `/api/*`
- Serve the frontend at `/`

## API

### POST `/api/detect`

**Request:**
```json
{ "text": "Bonjour le monde" }
```

**Response:**
```json
{
  "language": "French",
  "confidence": 99.8,
  "input_text": "Bonjour le monde"
}
```

### GET `/api/health`
Returns `{ "status": "ok" }` — useful for uptime checks.
