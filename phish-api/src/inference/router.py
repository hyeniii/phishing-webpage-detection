from fastapi import APIRouter
from src.inference import schemas, models

router = APIRouter()

@router.post('/predict', response_model=schemas.Prediction)
async def get_prediction(url_input: schemas.UrlInput):
    prediction = models.predict_and_save(url_input.url)
    return {"prediction": prediction}