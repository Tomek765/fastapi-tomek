from fastapi import FastAPI, Query
from datetime import datetime
import openai
import os

app = FastAPI()

# 🔐 KLUCZ API OpenAI – wpisz swój własny klucz tutaj:
openai.api_key = os.getenv("OPENAI_API_KEY")

# Dane przykładowe – później podpinamy prawdziwe źródła
dane_spolek = {
    "CDPROJEKT": {"kurs": 192.10, "zmiana": "+1.34%", "RSI": 58.2, "MACD": "Buy", "wolumen": "213 000"},
    "ASBIS": {"kurs": 29.80, "zmiana": "-0.62%", "RSI": 44.7, "MACD": "Sell", "wolumen": "94 000"},
    "PKN": {"kurs": 78.55, "zmiana": "+0.89%", "RSI": 65.1, "MACD": "Buy", "wolumen": "321 000"},
    "BIOCELTIX": {"kurs": 36.20, "zmiana": "-2.14%", "RSI": 27.3, "MACD": "Sell", "wolumen": "62 000"}
}

@app.get("/")
def root():
    return {"message": "Witaj w AI Analizatorze Tomka – wersja FASTAPI+GPT 🔥"}

@app.get("/analiza_ai")
def analiza_ai(spolka: str = Query(..., description="Nazwa spółki")):
    spolka = spolka.upper()
    if spolka not in dane_spolek:
        return {"error": f"Nie mam danych dla spółki '{spolka}'."}

    dane = dane_spolek[spolka]
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    prompt = f"""
    Jesteś ulicznym analitykiem giełdowym. Na podstawie poniższych danych powiedz, czy warto KUPIĆ, SPRZEDAĆ czy TRZYMAĆ akcje spółki {spolka}.
    Odpowiedź sarkastyczna, zabawna, z przekleństwami, ale z sensem – jakbyś tłumaczył kumplowi na piwie.

    Dane:
    - Kurs: {dane['kurs']} zł
    - Zmiana dzienna: {dane['zmiana']}
    - RSI: {dane['RSI']}
    - MACD: {dane['MACD']}
    - Wolumen: {dane['wolumen']}

    Twoja rekomendacja:
    """

    try:
        odpowiedz = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.9
        )
        gpt_output = odpowiedz.choices[0].message.content.strip()
    except Exception as e:
        return {"error": f"Błąd połączenia z OpenAI: {str(e)}"}

    return {
        "spolka": spolka,
        "dane": dane,
        "timestamp": timestamp,
        "rekomendacja_ai": gpt_output
    }
