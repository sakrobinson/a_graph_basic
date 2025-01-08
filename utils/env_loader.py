from dotenv import load_dotenv
import os

def load_env_vars():
    # Get the directory containing the current file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Go up one directory to the project root
    project_root = os.path.dirname(current_dir)
    # Path to .env file
    env_path = os.path.join(project_root, '.env')
     # Debug print to verify paths
    print(f"Looking for env file at: {env_path}")
    print(f"File exists: {os.path.exists(env_path)}")
    
    # Load the environment variables
    load_dotenv(env_path)

def get_api_key(key_name):
    api_key = os.getenv(key_name)
    if not api_key:
        raise ValueError(f"{key_name} not found in environment variables")
    return api_key 