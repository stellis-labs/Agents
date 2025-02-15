import requests
import re

class QueryParser:
    """Parses user queries using Ollama API"""

    def __init__(self, config):
        self.api_url = config.get_api_url()

    def parse(self, query):
        """Extracts key analysis targets from user query"""
        prompt = f"""Extract the key factors or entities that need to be analyzed from the following user query.
        Return only the key terms in a comma-separated format with no additional text.

        Query: {query}
        Response:"""

        response = requests.post(
            self.api_url,
            json={
                "model": "tinyllama",
                "prompt": prompt,
                "system": "You are a helpful assistant that extracts key analysis targets from user queries.",
                "stream": False
            }
        )

        response_text = response.json()["response"]

        # Extract only terms using regex (removes numbers, special characters, etc.)
        extracted_terms = re.findall(r'\b[A-Za-z0-9-]+\b', response_text)

        # Remove common stop words if necessary (optional)
        stop_words = {"the", "in", "a", "an", "of", "to", "on", "by", "for", "with", "and", "or"}
        cleaned_terms = [term for term in extracted_terms if term.lower() not in stop_words]

        return [f"Analyze {term.strip()}" for term in cleaned_terms]