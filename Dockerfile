# Używamy oficjalnego Pythona
FROM python:3.11

# Ustawiamy katalog roboczy
WORKDIR /app

# Kopiujemy wszystko z repozytorium do środka kontenera
COPY . .

# Instalujemy zależności
RUN pip install --upgrade pip && pip install -r requirements.txt

# Odpalamy aplikację FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
