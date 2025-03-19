import os
from dotenv import load_dotenv

class Config:
    """Loads environment variables and sets up API configuration"""

    def __init__(self):
        load_dotenv()
        self.api_url = "http://localhost:11434/api/generate"

    def get_api_url(self):
        return self.api_url