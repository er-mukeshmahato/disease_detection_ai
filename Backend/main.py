from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from supabase import Client
from app.api import api_router
from app.db.session import get_supabase

app = FastAPI(title="Disease Detection API")

# ✅ Allow requests from frontend (replace * with frontend URL in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Include routers
app.include_router(api_router)

# ✅ Database connection test
@app.get("/db-test")
def test_db(supabase: Client = Depends(get_supabase)):
    """
    Test if Supabase is connected and the 'prediction' table is accessible.
    """
    try:
        response = supabase.table("prediction").select("*").limit(1).execute()
        if hasattr(response, "data") and response.data:
            return {
                "status": "✅ Database connection working!",
                "sample_record": response.data
            }
        else:
            return {"status": "⚠️ Connected, but no data found in prediction table."}
    except Exception as e:
        return {"status": "❌ Database connection error!", "error": str(e)}

# ✅ Root endpoint
@app.get("/")
def root():
    return {
        "message": "✅ Disease Detection API is running!",
        "available_endpoints": {
            "db_test": "/db-test",
            "prediction_upload": "/predict/upload/",
            "backend_health": "/ok",
        },
    }
