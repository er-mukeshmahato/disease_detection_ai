# app/user_client.py

from app.db.client import supabase  # reuse the same client


def save_user(name: str, email: str, prediction_id: str):
    res = (
        supabase.table("user")
        .insert({
            "name": name,
            "email": email,
            "prediction_id": prediction_id
        })
        .execute()
    )
    return res.data[0] if res.data else None
