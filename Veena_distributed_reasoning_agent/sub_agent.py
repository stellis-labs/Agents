import re
import requests
import json
from rich.console import Console

console = Console()

class SubAgent:
    def __init__(self, name: str, task_type: str, task_prompt: str):
        """
        Initializes a SubAgent with its name, a brief description (task_type),
        and detailed task instructions (task_prompt).
        """
        self.name = name
        self.task_type = task_type
        self.task_prompt = task_prompt
        self.llm_model = "llama3"

    def execute(self, problem: str) -> str:
        """
        Executes the sub-agent's task by sending a prompt (combining its task_prompt with the overall problem)
        to the LLM and returns the final answer.
        """
        prompt = f"""Task for {self.name} ({self.task_type}):
{self.task_prompt}

Problem Context:
{problem}

Provide your final answer in no more than 5 concise sentences.
"""
        result = query_ollama(prompt)
        result = re.sub(r'[\x00-\x1f]+', ' ', result)
        return result

    def to_dict(self) -> dict:
        """
        Returns the sub-agent's configuration as a dictionary.
        """
        return {
            "name": self.name,
            "task_type": self.task_type,
            "task_prompt": self.task_prompt
        }

def query_ollama(prompt: str) -> str:
    """
    Sends a prompt to the LLM via the Ollama API and returns the generated response.
    """
    url = "http://localhost:11434/api/generate"
    headers = {"Content-Type": "application/json"}
    payload = {"model": "llama3", "prompt": prompt, "stream": True}
    try:
        response = requests.post(url, json=payload, headers=headers, stream=True)
        response.raise_for_status()
        result = ""
        for line in response.iter_lines():
            if line:
                decoded_line = line.decode("utf-8")
                data = json.loads(decoded_line)
                result += data.get("response", "")
                if data.get("done"):
                    break
        return result.strip()
    except Exception as e:
        console.print(f"[red]Error in query_ollama: {e}[/red]")
        return ""
