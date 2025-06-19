from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import openai

app = FastAPI()

# === 🔐 Wklej swój klucz API do OpenAI tutaj:
openai.api_key = "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"


# === 🧠 Dane wejściowe od użytkownika
class DaneAnalizy(BaseModel):
    ticker: str
    okres: str = "7 dni"

# === 📈 Pobieranie danych ze stooq
def pobierz_cene_akcji(ticker: str) -> float:
    url = f"https://stooq.pl/q/l/?s={ticker.lower()}.pl&f=sd2t2ohlcv&h&e=csv"
    response = requests.get(url)
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Błąd pobierania danych ze stooq.")
    linie = response.text.splitlines()
    if len(linie) < 2 or "N/D" in linie[1]:
        raise HTTPException(status_code=404, detail="Brak danych dla tej spółki.")
    dane = linie[1].split(",")
    return float(dane[6])  # Close price

# === 🤖 Analiza z GPT
def analiza_gpt(ticker: str, cena: float, okres: str) -> str:
    prompt = (
        f"Jesteś analitykiem finansowym. Przeanalizuj spółkę giełdową {ticker} "
        f"na podstawie jej aktualnej ceny {cena} zł i napisz krótką prognozę inwestycyjną "
        f"na okres {okres}. Zastosuj styl zrozumiały, dynamiczny, z podsumowaniem w punktach."
    )
    odpowiedz = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return odpowiedz['choices'][0]['message']['content']

# === 🚀 Endpoint główny
@app.post("/analiza")
def analizuj(dane: DaneAnalizy):
    cena = pobierz_cene_akcji(dane.ticker)
    wynik = analiza_gpt(dane.ticker, cena, dane.okres)
    return {
        "spolka": dane.ticker,
        "cena": f"{cena:.2f} zł",
        "analiza": wynik
    }

# === 🧪 Testowy GET
@app.get("/")
def przywitanie():
    return {"message": "Działa! To jest Tomek – wersja FastAPI z GPT i Stooq"}
