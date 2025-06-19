from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import openai

openai.api_key = "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"

app = FastAPI()

class RequestData(BaseModel):
    ticker: str
    okres: str = "7 dni"

def get_price(ticker):
    url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={ticker}.WA"
    r = requests.get(url).json()
    try:
        return r['quoteResponse']['result'][0]['regularMarketPrice']
    except:
        raise HTTPException(status_code=404, detail="Nie znaleziono spółki.")

@app.post("/analiza")
async def analiza_spolki(data: RequestData):
    price = get_price(data.ticker)
    prompt = f"Analizuj GPW: {data.ticker}, cena: {price} zł, okres: {data.okres}. Czy warto kupić?"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Jesteś analitykiem GPW."},
            {"role": "user", "content": prompt}
        ]
    )
    return {"analiza": response['choices'][0]['message']['content']}
