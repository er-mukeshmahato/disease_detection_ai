from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

# ======================
# Request Models
# ======================
class LoginRequest(BaseModel):
    email: str
    password: str


class RegisterRequest(BaseModel):
    email: str
    password: str


# ======================
# Routes
# ======================
@router.post("/login")
def login(data: LoginRequest):
    """
    User login endpoint
    """
    # TEMP logic (replace with Supabase / DB)
    if data.email == "admin@example.com" and data.password == "admin":
        return {"message": "Login successful"}
    
    raise HTTPException(status_code=401, detail="Invalid credentials")


@router.post("/register")
def register(data: RegisterRequest):
    """
    User registration endpoint
    """
    # TEMP logic
    return {
        "message": "User registered successfully",
        "email": data.email
    }
