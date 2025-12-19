# app/prediction_client.py

from app.db.client import supabase  # import the single instance


def save_prediction(image_url: str, predicted_class: str, confidence: float, all_confidences: dict):
    res = (
        supabase.table("prediction")
        .insert({
            "image_url": image_url,
            "predicted_class": predicted_class,
            "confidence": confidence,
            "all_confidences": all_confidences
        })
        .execute()
    )
    return res.data[0] if res.data else None


def get_prediction_by_id(prediction_id: str):
    res = (
        supabase.table("prediction")
        .select("*")
        .eq("id", prediction_id)
        .single()
        .execute()
    )
    return res.data
