from fastapi import APIRouter, UploadFile, File, Form
from decouple import config
import uuid
import numpy as np
import cv2
from io import BytesIO
from supabase import create_client, Client
from fastapi.responses import StreamingResponse, JSONResponse
from PIL import Image
import requests
import tensorflow as tf
from app.ml.gradcam  import load_image_from_url, generate_gradcam , overlay_heatmap

from app.ml.model_loader import load_model
from app.ml.predict import predict_disease, load_and_preprocess, generate_comparison_report_pdf, compute_gradcam

router = APIRouter()

# -----------------------------
# Load environment variables
# -----------------------------
SUPABASE_URL = config("SUPABASE_URL")
SUPABASE_KEY = config("SUPABASE_KEY")

# -----------------------------
# Initialize Supabase client
# -----------------------------
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# -----------------------------
# Class names
# -----------------------------
CLASS_NAMES = ['Covid', 'Normal', 'Pneumonia', 'Pneumothorax', 'Tuberculosis']

# -----------------------------
# Load model once at startup
# -----------------------------
model = load_model()


# ===============================
# Upload & Predict
# # ===============================
# @router.post("/upload/")
# async def upload_image(file: UploadFile = File(...)):
#     try:
#         contents = await file.read()
#         unique_filename = f"{uuid.uuid4()}_{file.filename}"

#         # Upload original image to Supabase Storage
#         supabase.storage.from_("predictions").upload(
#             unique_filename, contents, {"content-type": "image/jpeg"}
#         )
#         file_url = supabase.storage.from_("predictions").get_public_url(unique_filename)

#         # Predict disease
#         class_index, confidence, all_confidence = predict_disease(model, contents)
#         class_name = CLASS_NAMES[class_index]

#         # Save in Supabase table
#         response = supabase.table("prediction").insert({
#             "image_url": file_url,
#             "predicted_label": class_name,
#             "confidence": confidence,
#             "all_confidence": all_confidence
#         }, returning="representation").execute()

#         return {
#             'data': response.data[0],
#             "predicted_label": class_name,
#             "confidence": round(confidence, 4),
#             "all_confidence": {CLASS_NAMES[i]: round(all_confidence[i], 4) for i in range(len(CLASS_NAMES))}
#         }

#     except Exception as e:
#         return {"status": "❌ Error", "error": str(e)}
@router.post("/upload/")
async def upload_image(file: UploadFile = File(...)):

    try:
        contents = await file.read()
        unique_filename = f"{uuid.uuid4()}_{file.filename}"

        # ---------------------------------------------
        # 1. Upload ORIGINAL image to Supabase Storage
        # ---------------------------------------------
        supabase.storage.from_("predictions").upload(
            unique_filename, contents, {"content-type": file.content_type}
        )
        file_url = supabase.storage.from_("predictions").get_public_url(unique_filename)

        # ---------------------------------------------
        # 2. Predict disease
        # ---------------------------------------------
        class_index, confidence, all_confidence = predict_disease(model, contents)
        class_name = CLASS_NAMES[class_index]

        # ---------------------------------------------
        # 3. Insert initial record (WITHOUT GradCAM)
        # ---------------------------------------------
        created = supabase.table("prediction").insert({
            "image_url": file_url,
            "predicted_label": class_name,
            "confidence": confidence,
            "all_confidence": all_confidence
        }, returning="representation").execute()

        record = created.data[0]
        image_url = record["image_url"]

        if image_url is None:
            raise Exception("Image URL is None after upload.")

        # ---------------------------------------------
        # 4. Load Original Image from URL
        # ---------------------------------------------
        img = load_image_from_url(image_url)

        # ---------------------------------------------
        # 5. Generate Grad-CAM
        # ---------------------------------------------
        heatmap, preds, idx = generate_gradcam(model, img)
        gradcam = overlay_heatmap(img, heatmap)

        # Convert GradCAM numpy → bytes
        _, encoded_img = cv2.imencode(".jpg", gradcam)
        gradcam_bytes = encoded_img.tobytes()

        # Unique name
        gradcam_filename = f"gradcam_{uuid.uuid4()}.jpg"

        # ---------------------------------------------
        # 6. Upload Grad-CAM image to 'grad_cam' bucket
        # ---------------------------------------------
        supabase.storage.from_("grad_cam").upload(
            gradcam_filename,
            gradcam_bytes,
            {"content-type": "image/jpeg"}
        )
        gradcam_url = supabase.storage.from_("grad_cam").get_public_url(gradcam_filename)

        # ---------------------------------------------
        # 7. UPDATE RECORD with GradCAM URL
        # ---------------------------------------------
        supabase.table("prediction").update({
            "gradcam_url": gradcam_url
        }).eq("id", record["id"]).execute()

        # ---------------------------------------------
        # 8. Return response
        # ---------------------------------------------
        return {
            "image_url": file_url,
            "gradcam_url": gradcam_url,
            "predicted_label": class_name,
            "confidence": round(confidence, 4),
            "all_confidence": {
                CLASS_NAMES[i]: round(float(all_confidence[i]), 4)
                for i in range(len(CLASS_NAMES))
            }
        }

    except Exception as e:
        return {"status": "❌ Error", "error": str(e)}

    
                



# ===============================
# Health check
# ===============================
@router.get("/ok")
async def ok():
    return {"status": "✅ Prediction API is working!"}


# ===============================
# Grad-CAM explanation
# ===============================
@router.post("/explain/")
async def explain(prediction_id: str = Form(...)):
    try:
        # Fetch prediction row from Supabase
        response = supabase.table("prediction").select("*").eq("id", prediction_id).execute()
        if not response.data:
            return JSONResponse({"status": "❌ Error", "error": "Prediction not found"}, status_code=404)

        row = response.data[0]
        image_url = row.get("image_url")
        if not image_url:
            return JSONResponse({"status": "❌ Error", "error": "Original image URL not found"}, status_code=404)

        # Download and preprocess image
        resp = requests.get(image_url)
        img = Image.open(BytesIO(resp.content)).convert("RGB")
        img = img.resize((224, 224))
        x = np.expand_dims(np.array(img, dtype=np.float32) / 255.0, axis=0)
        x_tensor = tf.convert_to_tensor(x, dtype=tf.float32)

        preds = model([x_tensor])
       # Extract the real prediction array
        pred_array = preds[0]        # tuple element
        pred_vector = pred_array[0]  # first batch entry

        # Get predicted class
        predicted_class_index = int(np.argmax(pred_vector))
        predicted_class = CLASS_NAMES[predicted_class_index]

        # Grad-CAM
        heatmap = compute_gradcam(model, x_tensor, predicted_class_index, last_conv_layer_name="block5_conv3")

        # Convert heatmap to bytes and upload
        _, buffer = cv2.imencode(".jpg", heatmap)
        heatmap_bytes = buffer.tobytes()
        heatmap_filename = f"{uuid.uuid4()}.jpg"
        supabase.storage.from_("grad_cam").upload(
            heatmap_filename, heatmap_bytes, {"content-type": "image/jpeg"}
        )
        heatmap_url = supabase.storage.from_("grad_cam").get_public_url(heatmap_filename)

        # Update prediction row
        supabase.table("prediction").update({"heatmap_url": heatmap_url}).eq("id", prediction_id).execute()

        return {
            "predicted_class": predicted_class,
            "all_confidence": all_confidence,
            "heatmap_url": heatmap_url
        }

    except Exception as e:
        return JSONResponse({"status": "❌ Grad-CAM Error", "error": str(e)}, status_code=500)

# ===============================
# Download PDF report
# ===============================
@router.post("/download-report/")
async def download_report(
    prediction_id: str = Form(...),
    name: str = Form(...),
    email: str = Form(...)
):
    try:
        # Fetch record
        response = supabase.table("prediction").select("*").eq("id", prediction_id).execute()
        if response.error:
            return JSONResponse({"status": "❌ Error fetching data", "error": str(response.error)}, status_code=500)

        data_list = response.data
        if not data_list:
            return JSONResponse({"status": "❌ Not Found"}, status_code=404)

        record = data_list[0]

        # Generate PDF
        pdf_buffer: BytesIO = generate_comparison_report_pdf(
            name=name,
            email=email,
            prediction=record.get("predicted_label", "Unknown"),
            confidence=float(record.get("confidence", 0)),
            all_confidence=record.get("all_confidence", {}),
            original_image_path=record.get("image_url", None),
            heatmap_url=record.get("heatmap_url", None)
        )

        return StreamingResponse(
            pdf_buffer,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=Xray_Report_{prediction_id}.pdf"},
        )

    except Exception as e:
        return JSONResponse({"status": "❌ Error", "error": str(e)}, status_code=500)
