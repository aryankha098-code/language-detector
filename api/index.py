from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import fasttext
import re
import os

app = FastAPI(title="Language Detector API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

# Load model once at startup
MODEL_PATH = os.path.join(os.path.dirname(__file__), "language_detector.bin")
model = None

def get_model():
    global model
    if model is None:
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(f"Model not found at {MODEL_PATH}")
        model = fasttext.load_model(MODEL_PATH)
    return model

def preprocess(text: str) -> str:
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r' +', ' ', text)
    return text.strip().lower()

class TextInput(BaseModel):
    text: str

class PredictionResponse(BaseModel):
    language: str
    confidence: float
    input_text: str

@app.get("/")
def root():
    return {"status": "Language Detector API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/detect", response_model=PredictionResponse)
def detect_language(payload: TextInput):
    if not payload.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    try:
        mdl = get_model()
        processed = preprocess(payload.text)
        labels, probs = mdl.predict(processed, k=1)

        # Strip __label__ prefix
        language = labels[0].replace("__label__", "")
        confidence = float(probs[0])

        return PredictionResponse(
            language=language,
            confidence=round(confidence * 100, 2),
            input_text=payload.text
        )
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")
