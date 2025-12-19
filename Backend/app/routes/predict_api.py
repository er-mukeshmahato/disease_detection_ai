from fastapi import APIRouter, UploadFile, File
import uuid
import cv2
import json
from decouple import config
import numpy as np
from io import BytesIO
from PIL import Image
from app.ml.model_loader import model_load
from app.ml.gradcam import generate_gradcam, overlay_heatmap
from supabase import create_client, Client
from app.ml.predict import predict_disease
import tensorflow as tf
from fastapi import APIRouter, HTTPException, Form
from fastapi.responses import FileResponse
from app.ml.ai_explanation import load_heatmap, determine_heatmap_focus, ai_explanation

from app.db.prediction_client import get_prediction_by_id
from app.db.user_client import save_user
from app.ml.report import generate_pdf_report

# ---------------------------------------------------------
# CONFIG + GLOBALS
# ---------------------------------------------------------

CLASS_NAMES = ['Covid', 'Normal', 'Pneumonia', 'Pneumothorax', 'Tuberculosis']

SUPABASE_URL = config("SUPABASE_URL")
SUPABASE_KEY = config("SUPABASE_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
router = APIRouter()

# Load model once
model = model_load()

# ---------------------------------------------------------
# ROUTES
# ---------------------------------------------------------

@router.post("/upload/")
async def upload_image(file: UploadFile = File(...)):

    # READ FILE
    contents = await file.read()
    unique_filename = f"{uuid.uuid4()}_{file.filename}"

    # UPLOAD ORIGINAL IMAGE
    supabase.storage.from_("predictions").upload(
        unique_filename,
        contents,
        {"content-type": file.content_type}
    )
    file_url = supabase.storage.from_("predictions").get_public_url(unique_filename)

    # PREDICT
    x, class_index, confidence, all_confidence, pil_image = predict_disease(model, contents)
    class_name = CLASS_NAMES[class_index]

    # STORE PREDICTION IN DB
    all_conf_str = json.dumps(all_confidence)
    created = supabase.table("prediction").insert({
        "image_url": file_url,
        "predicted_label": class_name,
        "confidence": float(confidence),
        "all_confidence": all_conf_str
    }).execute()

    record = created.data[0]
    final_conf = record["all_confidence"]
    if isinstance(final_conf, str):
        final_conf = json.loads(final_conf)
    final_conf = [float(v) for v in final_conf]

    # GENERATE GRAD-CAM
    heatmap = generate_gradcam(model, x, class_index)
    print(type(heatmap))
    
    gradcam_np = overlay_heatmap(pil_image, heatmap)

    ok, encoded = cv2.imencode(".jpg", gradcam_np)
    gradcam_bytes = encoded.tobytes()
    gradcam_filename = f"gradcam_{uuid.uuid4()}.jpg"

    # UPLOAD GRAD-CAM
    supabase.storage.from_("grad_cam").upload(
        gradcam_filename,
        gradcam_bytes,
        {"content-type": "image/jpeg"}
    )
    gradcam_url = supabase.storage.from_("grad_cam").get_public_url(gradcam_filename)
    heatmap = load_heatmap(gradcam_url)
    focus = determine_heatmap_focus(heatmap)
    description = ai_explanation(class_name, confidence, focus)

    # UPDATE RECORD WITH GRADCAM URL
    supabase.table("prediction").update({
        "gradcam_url": gradcam_url,
        "explanation": description
    }).eq("id", record["id"]).execute()

   

    # RETURN RESPONSE
    return {
        "id": record["id"],
        "image_url": file_url,
        "gradcam_url": gradcam_url,
        "predicted_label": class_name,
        "confidence": round(float(confidence), 4),
        "explanation:": description
    }


@router.post("/download-report/")
async def download_report(
    prediction_id: str = Form(...),
    name: str = Form(...),
    email: str = Form(...)
):
    # Save user into database
    try:
        save_user(name=name, email=email, prediction_id=prediction_id)
    except Exception as e:
        raise HTTPException(500, f"Failed to save user: {str(e)}")

    # Fetch prediction record
    record = get_prediction_by_id(prediction_id)
    if not record:
        raise HTTPException(404, "Prediction ID not found")

    # Extract fields
    image_url = record.get("image_url")
    gradcam_url = record.get("gradcam_url")
    predicted_label = record.get("predicted_label")
    confidence = record.get("confidence")
    all_confidence = record.get("all_confidence", {})
    explanation= record.get("explanation", "")

     # Validate URLs

    if not image_url or not gradcam_url:
        raise HTTPException(400, "Missing image_url or gradcam_url")

    # Generate PDF
    pdf_path = generate_pdf_report(
        image_url=image_url,
        gradcam_url=gradcam_url,
        predicted_label=predicted_label,
        confidence=confidence,
        explanation=explanation,
        name=name,
        email=email
    )

    # Return PDF file
    return FileResponse(
        pdf_path,
        filename="xray_report.pdf",
        media_type="application/pdf"
    )
