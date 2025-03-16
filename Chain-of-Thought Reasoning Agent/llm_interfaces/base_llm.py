from abc import ABC, abstractmethod

class BaseLLM(ABC):
    """ Abstract Base Class for LLMs (Ollama, Groq, etc.) """

    @abstractmethod
    def run(self, prompt: str) -> str:
        """ Method to send a prompt and receive a response. """
        pass