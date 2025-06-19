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
    try:
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
    except Exception as e:
        return {"error": str(e)}
