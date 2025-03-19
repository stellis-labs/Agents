import logging
import json5
from typing import List, Dict, Any
from agents.base import LLMBaseAgent
from utils.helpers import clean_response

class TrailblazerAgent(LLMBaseAgent):
    def evaluate(self, candidates: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        prompt = (
            "Role: Trailblazer.\n"
            "Task: For the given candidate solutions (a JSON array of objects with a 'candidate' field), "
            "return a JSON array of objects. Each object must include the same 'candidate' field and add two fields: "
            "'pheromone_label' (one of \"high\", \"medium\", or \"low\") and 'pheromone_value' (a numeric value).\n"
            f"Input: {json5.dumps(candidates)}\n"
            "Return only valid JSON with no additional commentary."
        )
        response = self._llm_call(prompt, temperature=0.7)
        cleaned = clean_response(response)
        try:
            evaluated = json5.loads(cleaned)
            if not isinstance(evaluated, list):
                raise ValueError("Response is not a JSON array.")
            logging.info(f"Trailblazer evaluation: {evaluated}")
            return evaluated
        except Exception as e:
            logging.error(f"Trailblazer parsing error. Raw response: {response}\nCleaned response: {cleaned}\nException: {e}")
            raise
