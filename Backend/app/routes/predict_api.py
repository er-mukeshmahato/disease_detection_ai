from fastapi import APIRouter, UploadFile, File
from app.ml.model_loader import load_model
from app.ml.predict import predict_disease

router = APIRouter()


CLASS_NAMES = ['Covid', 'Normal', 'Pneumonia', 'Pneumothorax', 'Tuberculosis']

# Load the model once at startup
model = load_model()

@router.post("/upload/")
async def predict_image(file: UploadFile = File(...)):
    contents = await file.read()
    class_index = predict_disease(model, contents)
    class_name = CLASS_NAMES[class_index]
    return {"class_name": class_name}

@router.get("/ok")
async def ok():
    return {"status": "Prediction API is working!"}
