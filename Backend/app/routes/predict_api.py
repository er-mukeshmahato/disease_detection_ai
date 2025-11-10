from fastapi import APIRouter, UploadFile, File
from app.ml.model_loader import load_model
from app.ml.predict import predict_disease
import os
from tensorflow.keras.models import load_model

# Get the absolute path to the current file's directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

router = APIRouter()

# Path to your trained model
MODEL_PATH = os.path.join(BASE_DIR, "app", "ml", "chest_disease_model.h5")
CLASS_NAMES = ['Covid', 'Normal', 'Pneumonia', 'Pneumothorax', 'Tuberculosis']

# Load the model once at startup
model = load_model(MODEL_PATH)

@router.post("/upload/")
async def predict_image(file: UploadFile = File(...)):
    contents = await file.read()
    class_index = predict_disease(model, contents)
    class_name = CLASS_NAMES[class_index]
    return {"class_name": class_name}

@router.get("/ok")
async def ok():
    return {"status": "Prediction API is working!"}
