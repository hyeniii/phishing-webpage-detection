from pydantic import BaseModel

class UrlInput(BaseModel):
    url: str

class Prediction(BaseModel):
    prediction: int