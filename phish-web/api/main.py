from fastapi import FastAPI
from src.inference.router import router

app= FastAPI()

app.include_router(router)