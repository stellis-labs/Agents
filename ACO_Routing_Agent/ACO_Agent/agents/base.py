import logging
from groq import Groq

class LLMBaseAgent:
    def __init__(self, api_key: str, model: str = "deepseek-r1-distill-llama-70b"):
        self.api_key = api_key
        self.model = model
        self.client = Groq(api_key=api_key)
    
    def _llm_call(self, prompt: str, temperature: float = 0.7) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature,
                max_tokens=2000
            )
            logging.info(f"LLM call prompt: {prompt}")
            raw = response.choices[0].message.content.strip()
            logging.info(f"LLM call raw response: {raw}")
            return raw
        except Exception as e:
            logging.error(f"LLM call error: {str(e)}")
            raise RuntimeError("LLM call failed.")
