import logging
import json
import json5
from typing import Dict, List, Any
from utils.helpers import clean_response
from agents.base import LLMBaseAgent

class ExplorerAgent(LLMBaseAgent):
    def __init__(self, api_key: str, model: str, constraints: str, max_solutions: int = 5):
        super().__init__(api_key, model)
        self.constraints = constraints
        self.max_solutions = max_solutions

    def explore(self, problem_definition: str, count: int) -> List[Dict[str, Any]]:
        prompt = (
            f"Role: Explorer.\n"
            f"Task: Return a JSON array of potential solutions for the following problem:\n"
            f"{problem_definition}\n"
            f"Constraints: {self.constraints}\n"
            f"Return at most {self.max_solutions} solutions, each as a concise string (e.g., \"Route A\").\n"
            "Return only valid JSON with no additional commentary."
        )
        response = self._llm_call(prompt, temperature=0.7)
        cleaned = clean_response(response)
        try:
            solutions = json5.loads(cleaned)
            if not isinstance(solutions, list):
                raise ValueError("Response is not a JSON array.")
            logging.info(f"Explorer generated candidates: {solutions}")
            return [{"candidate": sol, "initial_score": 0.5} for sol in solutions if isinstance(sol, str)]
        except Exception as e:
            logging.error(f"Explorer parsing error. Raw response: {response}\nCleaned response: {cleaned}\nException: {e}")
            raise
