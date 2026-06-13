from fastapi import FastAPI
import joblib
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
import subprocess

if not os.path.exists("portland_crime_rf_model.pkl"):
    print("Model not found, training now...")
    subprocess.run(["python", "train.py"], check=True)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

loaded_model = joblib.load("portland_crime_rf_model.pkl")
loaded_encoder = joblib.load("neighborhood_label_encoder.pkl")

class CrimeInput(BaseModel):
    hour: int
    month: int
    latitude: float
    longitude: float
    neighborhood: str
    
@app.post("/predict")
def predict_crime(input_data: CrimeInput):
    try:
        neighborhood_encoded = loaded_encoder.transform([input_data.neighborhood])[0]
    except ValueError:
        neighborhood_encoded = loaded_encoder.transform(["Downtown"])[0]
    features = [[
        input_data.hour,
        neighborhood_encoded,
        input_data.month,
        input_data.longitude,
        input_data.latitude
    ]]
    prediction = loaded_model.predict(features)[0]
    return {"predicted_crime_type": prediction}