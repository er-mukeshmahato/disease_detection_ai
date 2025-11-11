from fastapi import APIRouter, UploadFile, File
from decouple import config
import uuid
from supabase import create_client, Client

from app.ml.model_loader import load_model
from app.ml.predict import predict_disease

router = APIRouter()

# ✅ Load environment variables
SUPABASE_URL = config("SUPABASE_URL")
SUPABASE_KEY = config("SUPABASE_KEY")

# ✅ Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ✅ Class labels
CLASS_NAMES = ['Covid', 'Normal', 'Pneumonia', 'Pneumothorax', 'Tuberculosis']

# ✅ Load ML model once
model = load_model()


@router.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    """
    Upload image to Supabase Storage, run prediction, save full record in DB,
    and return only predicted label + confidence to user.
    """
    try:
        # Read image bytes
        contents = await file.read()

        # Generate a unique filename
        unique_filename = f"{uuid.uuid4()}_{file.filename}"

        # ✅ Upload to Supabase Storage
        upload_resp = supabase.storage.from_("predictions").upload(unique_filename, contents)
        if upload_resp is None:
            return {"status": "❌ Failed to upload image"}

        # ✅ Get public URL
        file_url = supabase.storage.from_("predictions").get_public_url(unique_filename)

        # ✅ Predict disease
        class_index, confidence = predict_disease(model, contents)
        class_name = CLASS_NAMES[class_index]

        # ✅ Save full record in Supabase table
        supabase.table("prediction").insert({
            "image_url": file_url,          # full storage URL
            "predicted_label": class_name,  # model result
            "confidence": confidence        # probability
        }).execute()

        # ✅ Return only label + confidence
        return {
            "predicted_label": class_name,
            "confidence": round(confidence, 4)
        }

    except Exception as e:
        return {"status": "❌ Error", "error": str(e)}


@router.get("/ok")
async def ok():
    return {"status": "✅ Prediction API is working!"}
