from dotenv import load_dotenv
import os

# Load the .env file
load_dotenv()

# Read variables
app_name = os.getenv("APP_NAME")
secret_key = os.getenv("SECRET_KEY")
debug = os.getenv("DEBUG")

print(f"App: {app_name}")
print(f"Secret: {secret_key}")
print(f"Debug: {debug}")

# With a default fallback if variable is missing
port = os.getenv("PORT", "8000")
print(f"Port: {port}")