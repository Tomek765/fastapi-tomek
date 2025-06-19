from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random

app = FastAPI()

# CORS – żeby frontend mógł gadać z backendem
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DaneAnalizy(BaseModel):
    ticker: str
    okres: str

@app.get("/")
def przywitanie():
    return {"message": "Działa! To jest Tomek – wersja FastAPI"}

@app.post("/analiza")
def analiza_spolki(dane: DaneAnalizy):
    ticker = dane.ticker
    okres = dane.okres

    # PRZYKŁADOWA ANALIZA (tu wstawisz GPT lub prawdziwe dane później)
    odpowiedz = f"Analiza spółki **{ticker}** za okres **{okres}**: \n- Cena: {round(random.uniform(10, 200), 2)} zł\n- Prognoza: 🟢 Pozytywna (demo)"

    return {"analiza": odpowiedz}
