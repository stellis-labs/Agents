from groq import Groq

class QueryParser:
    """Parses user queries using LLM to extract actionable tasks"""
    
    def __init__(self, groq_client):
        self.groq_client = groq_client

    def parse(self, query):
        """Extracts key analysis targets from user query"""
        prompt = f"""Analyze the following user query and identify the key factors or entities that need to be analyzed. 
        Return your response as a comma-separated list of terms, each term being a noun or noun phrase. 
        Do not include any additional text.

        Query: {query}
        Response:"""
        
        response = self.groq_client.chat.completions.create(
            model="llama3-70b-8192",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that extracts key analysis targets from user queries."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
        )
        
        response_text = response.choices[0].message.content
        tasks = [f"Analyze {term.strip()}" for term in response_text.split(",") if term.strip()]
        return tasks