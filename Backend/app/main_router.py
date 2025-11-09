from fastapi import APIRouter
from app.auth.routes import router as auth_router
from app.routes import predict_api

api_router = APIRouter()

# include the authentication router
api_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])

# ✅ include the prediction router correctly
api_router.include_router(predict_api.router, prefix="/predict", tags=["Prediction"])
