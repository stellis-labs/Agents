import logging
from typing import Dict, Any

class ProblemInputProcessor:
    """Processes and analyzes the input problem."""
    
    def __init__(self, ollama_client, config):
        self.ollama_client = ollama_client
        self.config = config
        self.logger = logging.getLogger("FRA.InputLayer")
    
    def process(self, problem_statement: str) -> Dict[str, Any]:
        """
        Process the input problem statement.
        
        Args:
            problem_statement: The raw problem statement from the user
            
        Returns:
            Dict containing the processed problem with metadata
        """
        self.logger.info(f"Processing problem: {problem_statement}")
        
        instruction = """
        Analyze the given problem statement. Identify:
        1. The main objectives or goals
        2. Key constraints or requirements
        3. Domain or field of the problem
        4. Complexity level (1-10)
        5. Required knowledge areas
        """
        
        output_format = {
            "title": "A concise title for the problem",
            "objectives": ["List of main objectives"],
            "constraints": ["List of key constraints"],
            "domain": "The domain or field",
            "complexity": "Numeric rating from 1-10",
            "knowledge_areas": ["Required fields of knowledge"],
            "reformulated_statement": "A clear, reformulated version of the problem"
        }
        
        processed_problem = self.ollama_client.generate_structured(
            problem_statement, instruction, output_format
        )
        
        # Check if the response contains an error
        if "error" in processed_problem:
            self.logger.error(f"Failed to process problem: {processed_problem['error']}")
            self.logger.debug(f"Raw response: {processed_problem.get('raw_response', 'No raw response')}")
            return self._create_fallback_problem(problem_statement)
        
        # Ensure all required keys are present in the response
        required_keys = ["title", "objectives", "constraints", "domain", "complexity", "knowledge_areas", "reformulated_statement"]
        for key in required_keys:
            if key not in processed_problem:
                self.logger.warning(f"Processed problem is missing key: {key}")
                processed_problem[key] = f"Missing {key}"  # Provide a default value
        
        self.logger.info(f"Problem processed: {processed_problem['title']}")
        return processed_problem
    
    def _create_fallback_problem(self, problem_statement: str) -> Dict[str, Any]:
        """
        Create a fallback problem dictionary in case of API failure.
        
        Args:
            problem_statement: The raw problem statement from the user
            
        Returns:
            Dict containing a fallback problem with default values
        """
        self.logger.warning("Creating fallback problem due to API failure")
        return {
            "title": "Fallback Problem",
            "objectives": ["Analyze and solve the problem"],
            "constraints": ["Unknown constraints"],
            "domain": "General",
            "complexity": 5,
            "knowledge_areas": ["General knowledge"],
            "reformulated_statement": problem_statement
        }