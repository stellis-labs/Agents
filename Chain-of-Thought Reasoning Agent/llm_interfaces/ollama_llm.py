import time
from functools import lru_cache
import requests
import logging

logger = logging.getLogger(__name__)

class OllamaLLM:

    def __init__(self, model_name: str = "llama3.2", temperature: float = 0.7, api_url: str = "http://localhost:11434"):
        self.model_name = model_name
        self.temperature = temperature
        self.api_url = api_url
        logger.info(f"OllamaLLM initialized with model: {self.model_name}")

    @lru_cache(maxsize=100)  # Cache LLM responses to prevent redundant calls
    def run(self, prompt: str) -> str:
        """ Calls the LLM API and caches responses to prevent redundant computation. """
        time.sleep(1)  # Small delay to reduce overload on system
        logger.info(f"Sending prompt to {self.model_name}: {prompt}")
        payload = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": self.temperature
        }

        try:
            response = requests.post(f"{self.api_url}/v1/chat/completions", json=payload)
            response.raise_for_status()
            result = response.json()
            response_text = result['choices'][0]['message']['content']
            return response_text
        except requests.exceptions.RequestException as e:
            logger.error(f"Ollama API request failed: {e}")
            raise RuntimeError(f"Ollama API request failed: {e}")