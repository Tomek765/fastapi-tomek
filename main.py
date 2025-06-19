from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import openai
import os

# === Konfiguracja API OpenAI ===
openai.api_key = os.getenv("OPENAI_API_KEY")

# === Inicjalizacja FastAPI ===
app = FastAPI()

# === Middleware CORS ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 🔒 Możesz tu wstawić swoją domenę zamiast "*" dla większego bezpieczeństwa
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Model danych wejściowych ===
class DaneZapytania(BaseModel):
    zapytanie: str

# === Endpoint powitalny (GET) ===
@app.get("/")
async def root():
    return {"message": "Witaj w AI Analizatorze Tomka – wersja FASTAPI+GPT 🤖"}

# === Endpoint analizujący (POST) ===
@app.post("/analiza")
async def analiza(dane: DaneZapytania):
    try:
        odpowiedz = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Jesteś specjalistą od giełdy i analizujesz spółki z GPW."},
                {"role": "user", "content": f"Przeanalizuj spółkę: {dane.zapytanie}"}
            ]
        )
        tekst = odpowiedz["choices"][0]["message"]["content"]
        return {"odpowiedz": tekst}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
