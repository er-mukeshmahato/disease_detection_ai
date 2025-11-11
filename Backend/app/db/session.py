import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

def get_supabase() -> Client:
    """
    Returns a Supabase client instance for database operations.
    """
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("Supabase credentials are missing in environment variables.")
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return supabase
