from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import api_router  # combined router

app = FastAPI(title="Disease Detection API")

# Allow React frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers
app.include_router(api_router)


# Root endpoint: shows message and available routes
@app.get("/")
def root():
    endpoints = {
        "message": "API is running!",
        "available_endpoints": {
            "Auth": {
                "register": "/auth/register",
                "login": "/auth/login",
                "logout": "/auth/logout",
                "forgot_password": "/auth/forgot-password"
            },
            "Prediction": {
                "upload_image": "/predict/upload/",
                "prediction_health": "/predict/ok"
            },
            "Information": {
                "precautions": "/info/precautions/{disease_name}",
                "symptoms": "/info/symptoms/{disease_name}",
                "download_report": "/info/download_report/{disease_name}"
            },
            "Backend_health": "/ok"
        }
    }
    return endpoints

# Overall backend health check
@app.get("/ok")
def health_check():
    return {"status": "ok"}