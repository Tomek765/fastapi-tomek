from fastapi import FastAPI, Query
from typing import Optional
from datetime import datetime

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Działa! To jest Tomek – wersja FastAPI"}

@app.get("/analiza")
def analiza(spolka: str = Query(..., description="Nazwa spółki (np. CDPROJEKT)")):
    dane = {
        "CDPROJEKT": {"kurs": 192.10, "zmiana": "+1.34%", "RSI": 58.2, "MACD": "Buy", "wolumen": "213 000 szt."},
        "ASBIS": {"kurs": 29.80, "zmiana": "-0.62%", "RSI": 44.7, "MACD": "Sell", "wolumen": "94 000 szt."},
        "PKN": {"kurs": 78.55, "zmiana": "+0.89%", "RSI": 65.1, "MACD": "Buy", "wolumen": "321 000 szt."}
    }

    spolka = spolka.upper()
    if spolka not in dane:
        return {"error": f"Nie mam danych dla spółki '{spolka}'."}

    wynik = dane[spolka]
    wynik["spolka"] = spolka
    wynik["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M")

    return wynik
