from fastapi import FastAPI
from src.inference.router import router

app= FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(router)