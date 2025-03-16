from llm_interfaces.ollama_llm import OllamaLLM
from llm_interfaces.groq_llm import GroqLLM

def get_llm(provider: str, model_name: str = "llama3.2", api_key: str = None):
    """ Dynamically selects LLM provider (Ollama or Groq). """
    if provider.lower() == "ollama":
        return OllamaLLM(model_name=model_name)
    elif provider.lower() == "groq":
        if not api_key:
            raise ValueError("Groq API Key required for GroqLLM.")
        return GroqLLM(model_name=model_name, api_key=api_key)
    else:
        raise ValueError("Invalid LLM provider. Choose 'ollama' or 'groq'.")