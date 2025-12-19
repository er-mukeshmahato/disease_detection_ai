from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from app.api import api_router

# Load environment variables from .env
load_dotenv()

# =========================
# FastAPI App
# =========================
app = FastAPI(
    title="Disease Detection API",
    description="X-ray Disease Detection using TensorFlow + Grad-CAM",
    version="1.0.0",
)

# =========================
# CORS (important for React frontend)
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# Include API Routers
# =========================
app.include_router(api_router)

# =========================
# Health Check
# =========================
@app.get("/")
def root():
    return {
        "status": "OK",
        "message": "Disease Detection API is running"
    }
