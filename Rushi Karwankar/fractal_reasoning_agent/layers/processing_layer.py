import json
import logging
from typing import Dict, Any

class SolverUnit:
    """Solves individual sub-problems using domain-specific approaches."""
    
    def __init__(self, ollama_client, config):
        self.ollama_client = ollama_client
        self.config = config
        self.logger = logging.getLogger("FRA.SolverUnit")
    
    def solve(self, subproblem: Dict[str, Any]) -> Dict[str, Any]:
        """
        Solve a specific sub-problem.
        
        Args:
            subproblem: The sub-problem to solve
            
        Returns:
            Dict containing the solution
        """
        self.logger.info(f"Solving sub-problem: {subproblem.get('title', 'Untitled Subproblem')}")
        
        instruction = """
        Solve the given sub-problem. Provide a comprehensive solution that:
        1. Directly addresses the specific task
        2. Uses appropriate methods and approaches
        3. Explains reasoning and methodology
        4. Includes specific actionable steps
        """
        
        output_format = {
            "solution_id": f"SOL-{subproblem.get('id', 'UNKNOWN')}",
            "title": "Solution title",
            "approach": "Approach used to solve the problem",
            "solution_details": "Comprehensive description of the solution",
            "key_findings": ["List of important findings or insights"],
            "actionable_steps": ["List of specific actions to implement the solution"],
            "limitations": ["Potential limitations or caveats"],
            "confidence": "Numeric rating of confidence from 1-10"
        }
        
        try:
            solution = self.ollama_client.generate_structured(
                json.dumps(subproblem), instruction, output_format
            )
            self.logger.info(f"Solution generated for sub-problem {subproblem.get('id', 'UNKNOWN')}")
            return solution
        except Exception as e:
            self.logger.error(f"Failed to solve sub-problem: {e}")
            return {
                "error": "Failed to solve sub-problem",
                "details": str(e),
                "subproblem_id": subproblem.get("id", "UNKNOWN")
            }

class Evaluator:
    """Evaluates the quality and feasibility of solutions."""
    
    def __init__(self, ollama_client, config):
        self.ollama_client = ollama_client
        self.config = config
        self.logger = logging.getLogger("FRA.Evaluator")
    
    def evaluate(self, solution: Dict[str, Any], subproblem: Dict[str, Any]) -> Dict[str, Any]:
        """
        Evaluate a solution against the sub-problem's requirements.
        
        Args:
            solution: The solution to evaluate
            subproblem: The original sub-problem
            
        Returns:
            Dict containing the evaluation results
        """
        self.logger.info(f"Evaluating solution for: {subproblem.get('title', 'Untitled Subproblem')}")
        
        # Combine the subproblem and solution for context
        evaluation_context = {
            "subproblem": subproblem,
            "solution": solution
        }
        
        instruction = """
        Evaluate the provided solution against the sub-problem's requirements.
        Assess:
        1. Completeness - Does it fully address the sub-problem?
        2. Feasibility - Can it realistically be implemented?
        3. Effectiveness - How well would it solve the problem?
        4. Alignment - Does it align with the overall objectives?
        5. Risks - What are potential risks or downsides?
        """
        
        output_format = {
            "evaluation_id": f"EVAL-{solution.get('solution_id', 'UNKNOWN')}",
            "completeness_score": "Score from 1-10",
            "feasibility_score": "Score from 1-10",
            "effectiveness_score": "Score from 1-10",
            "alignment_score": "Score from 1-10",
            "overall_score": "Weighted average score from 1-10",
            "strengths": ["List of solution strengths"],
            "weaknesses": ["List of solution weaknesses"],
            "risks": ["List of potential risks"],
            "recommendations": ["Suggestions for improvement"]
        }
        
        try:
            evaluation = self.ollama_client.generate_structured(
                json.dumps(evaluation_context), instruction, output_format
            )
            self.logger.info(f"Evaluation completed with score {evaluation.get('overall_score', 'N/A')}")
            return evaluation
        except Exception as e:
            self.logger.error(f"Failed to evaluate solution: {e}")
            return {
                "error": "Failed to evaluate solution",
                "details": str(e),
                "solution_id": solution.get("solution_id", "UNKNOWN")
            }

class Optimizer:
    """Optimizes solutions based on evaluation feedback."""
    
    def __init__(self, ollama_client, config):
        self.ollama_client = ollama_client
        self.config = config
        self.logger = logging.getLogger("FRA.Optimizer")
    
    def optimize(self, solution: Dict[str, Any], evaluation: Dict[str, Any]) -> Dict[str, Any]:
        """
        Optimize a solution based on evaluation feedback.
        
        Args:
            solution: The original solution
            evaluation: The evaluation results
            
        Returns:
            Dict containing the optimized solution
        """
        self.logger.info(f"Optimizing solution: {solution.get('title', 'Untitled Solution')}")
        
        # Skip optimization if the solution scored highly
        if float(evaluation.get('overall_score', 0)) >= 8.5:
            self.logger.info(f"Solution already scores highly ({evaluation.get('overall_score')}), skipping optimization")
            solution['optimized'] = False
            return solution
        
        # Combine the solution and evaluation for context
        optimization_context = {
            "original_solution": solution,
            "evaluation": evaluation
        }
        
        instruction = """
        Optimize the provided solution based on the evaluation feedback.
        Focus on:
        1. Addressing identified weaknesses
        2. Mitigating potential risks
        3. Implementing evaluation recommendations
        4. Enhancing the solution's strengths
        
        Provide a revised, improved solution that maintains the original approach
        but enhances its effectiveness and feasibility.
        """
        
        # Use the same format as the original solution but mark as optimized
        output_format = dict(solution)
        output_format['optimized'] = True
        output_format['optimization_notes'] = "Notes describing the optimization changes"
        
        try:
            optimized_solution = self.ollama_client.generate_structured(
                json.dumps(optimization_context), instruction, output_format
            )
            self.logger.info(f"Solution optimized based on evaluation feedback")
            return optimized_solution
        except Exception as e:
            self.logger.error(f"Failed to optimize solution: {e}")
            return {
                "error": "Failed to optimize solution",
                "details": str(e),
                "solution_id": solution.get("solution_id", "UNKNOWN")
            }