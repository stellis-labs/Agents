import os
from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("Please set your GROQ_API_KEY environment variable.")
