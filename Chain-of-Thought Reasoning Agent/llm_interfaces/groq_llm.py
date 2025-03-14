import requests
import logging
from llm_interfaces.base_llm import BaseLLM

logger = logging.getLogger(__name__)

class GroqLLM(BaseLLM):
    """ Groq Cloud API Client """

    def __init__(self, model_name="llama3.2", temperature=0.7, api_key=None, api_url="https://api.groq.com/v1/chat/completions"):
        self.model_name = model_name
        self.temperature = temperature
        self.api_key = api_key
        self.api_url = api_url
        if not self.api_key:
            raise ValueError("Groq API Key is required.")
        logger.info(f"GroqLLM initialized with model: {self.model_name}")

    def run(self, prompt: str) -> str:
        """ Calls the Groq LLM API and returns a response. """
        logger.info(f"Sending prompt to Groq ({self.model_name}): {prompt}")

        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": self.temperature
        }

        try:
            response = requests.post(self.api_url, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
            response_text = result['choices'][0]['message']['content']
            logger.info(f"Groq Response: {response_text}")
            return response_text
        except requests.exceptions.RequestException as e:
            logger.error(f"Groq API failed: {e}")
            raise RuntimeError(f"Groq API request failed: {e}")
