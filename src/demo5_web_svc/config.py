import os
from dotenv import load_dotenv

load_dotenv()

SERVICE_HOST = os.getenv("SERVICE_HOST", "0.0.0.0")
SERVICE_PORT = os.getenv("SERVICE_PORT", 8000)

# Added AUTH_SERVICE_URL to avoid hardcoded auth-service URL in login page
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://localhost:8081")
