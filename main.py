from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Działa! To jest Tomek – wersja FastAPI"}
