from dotenv import load_dotenv
import os

def load_env_vars():
    """Load environment variables from .env file"""
    load_dotenv()
    
def get_api_key(key_name: str) -> str:
    """Safely get API key from environment variables"""
    api_key = os.getenv(key_name)
    if not api_key:
        raise ValueError(f"{key_name} not found in environment variables")
    return api_key 