import json
import logging
import uuid
from typing import Dict, Any, List

class PrimaryDecomposer:
    """Decomposes the complex problem into sub-problems."""
    
    def __init__(self, ollama_client, config):
        self.ollama_client = ollama_client
        self.config = config
        self.logger = logging.getLogger("FRA.PrimaryDecomposer")
    
    def decompose(self, processed_problem: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Decompose the problem into sub-problems.
        
        Args:
            processed_problem: The processed problem statement
            
        Returns:
            List of sub-problems
        """
        self.logger.info(f"Decomposing problem: {processed_problem['title']}")
        
        instruction = """
        Break down the complex problem into 3-7 detailed, manageable sub-problems.
        Each sub-problem should:
        1. Address a distinct aspect of the main problem
        2. Be solvable independently
        3. Have clear input and output requirements
        4. Be specific enough to be directly solved without further decomposition
        5. Have clear success criteria
        """
        
        output_format = {
            "subproblems": [
                {
                    "id": "Unique identifier",
                    "title": "Sub-problem title",
                    "description": "Detailed description",
                    "objectives": ["List of objectives for this sub-problem"],
                    "input_requirements": ["Required inputs"],
                    "expected_output": "Description of expected solution",
                    "complexity": "Numeric rating from 1-10",
                    "dependencies": ["IDs of any sub-problems this depends on"],
                    "approach": "Suggested approach to solve",
                    "success_criteria": ["List of criteria to evaluate success"]
                }
            ]
        }
        
        decomposition_result = self.ollama_client.generate_structured(
            json.dumps(processed_problem), instruction, output_format
        )
        
        # Add unique IDs if not present
        for idx, subproblem in enumerate(decomposition_result.get("subproblems", [])):
            if not subproblem.get("id"):
                subproblem["id"] = f"SP-{idx+1}-{uuid.uuid4().hex[:6]}"
        
        self.logger.info(f"Problem decomposed into {len(decomposition_result.get('subproblems', []))} sub-problems")
        return decomposition_result.get("subproblems", [])