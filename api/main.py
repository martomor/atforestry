from fastapi import FastAPI, File, UploadFile
from .app.views import predict_land_cover


app = FastAPI(
    title='Atforesty Web API',
    description='This web interface allows the user to load an image predict cover land type',
    version="1.0.0"
)

@app.post("/v1/predict_image")
async def get_prediction(file: UploadFile = File(...)):
    image_file = await file.read()
    prediction = predict_land_cover(image_file)
    return prediction




