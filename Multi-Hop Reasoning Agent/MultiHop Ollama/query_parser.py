import requests

class QueryParser:
    """Parses user queries using LLM to extract actionable tasks"""
    
    def __init__(self):
        self.base_url = "http://localhost:11434/api/chat"

    def parse(self, query):
        """Extracts key analysis targets from user query"""
        prompt = f"""Analyze the following user query and identify the key factors or entities that need to be analyzed. 
        Return your response as a comma-separated list of terms, each term being a noun or noun phrase. 
        Do not include any additional text.

        Query: {query}
        Response:"""
        
        response = requests.post(
            self.base_url,
            json={
                "model": "tinyllama",
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant that extracts key analysis targets from user queries."},
                    {"role": "user", "content": prompt}
                ],
                "stream": False
            }
        )
        
        response_text = response.json()["message"]["content"]
        tasks = [f"Analyze {term.strip()}" for term in response_text.split(",") if term.strip()]
        return tasks