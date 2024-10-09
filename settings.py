from dotenv import load_dotenv
import os

load_dotenv()  # Loads variables from a .env file

ELEVATION_API_KEY = os.getenv('ELEVATION_API_KEY')