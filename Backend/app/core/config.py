import os

# Database URL (SQLite for dev)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./users.db")

# JWT Secret Key
SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key_here")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


