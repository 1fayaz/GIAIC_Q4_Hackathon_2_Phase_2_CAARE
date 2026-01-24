import os
from dotenv import load_dotenv

# Load the .env file
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

print(f"DATABASE_URL from environment: {os.getenv('DATABASE_URL')}")
print(f"Environment file loaded from: {dotenv_path}")
print(f"File exists: {os.path.exists(dotenv_path)}")