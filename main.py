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
