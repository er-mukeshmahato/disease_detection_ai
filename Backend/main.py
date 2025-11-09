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
