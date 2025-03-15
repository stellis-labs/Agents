import json
import logging
from typing import Dict, Any, List

class SolutionIntegrator:
    """Integrates sub-solutions into a comprehensive final solution."""
    
    def __init__(self, ollama_client, config):
        self.ollama_client = ollama_client
        self.config = config
        self.logger = logging.getLogger("FRA.SolutionIntegrator")
    
    def integrate(self, sub_solutions: List[Dict[str, Any]], processed_problem: Dict[str, Any]) -> Dict[str, Any]:
        """
        Integrate all sub-solutions into a cohesive final solution.
        
        Args:
            sub_solutions: List of all sub-solutions
            processed_problem: The original processed problem
            
        Returns:
            Dict containing the integrated solution
        """
        self.logger.info(f"Integrating {len(sub_solutions)} sub-solutions")
        
        # Prepare the integration context
        integration_context = {
            "original_problem": processed_problem,
            "sub_solutions": sub_solutions
        }
        
        instruction = """
        Integrate all sub-solutions into a comprehensive, cohesive final solution.
        The integrated solution should:
        1. Address all aspects of the original problem
        2. Resolve conflicts between sub-solutions
        3. Optimize for synergies between components
        4. Present a unified plan that leverages all insights
        5. Include implementation considerations and next steps
        """
        
        output_format = {
            "title": "Title for the integrated solution",
            "summary": "Executive summary of the solution (1-2 paragraphs)",
            "integrated_approach": "Comprehensive description of the integrated approach",
            "key_components": [
                {
                    "title": "Component title",
                    "description": "Component description",
                    "source_solutions": ["IDs of contributing sub-solutions"],
                    "implementation_steps": ["Specific implementation steps"]
                }
            ],
            "implementation_plan": {
                "phases": [
                    {
                        "phase": "Phase name",
                        "timeline": "Estimated timeline",
                        "key_activities": ["List of activities"],
                        "expected_outcomes": ["List of outcomes"]
                    }
                ]
            },
            "synergies": ["Identified synergies between components"],
            "addressed_conflicts": ["How conflicts between sub-solutions were resolved"],
            "success_metrics": ["Metrics to evaluate the success of the solution"]
        }
        
        integrated_solution = self.ollama_client.generate_structured(
            json.dumps(integration_context), instruction, output_format
        )
        
        self.logger.info("Solutions integrated successfully")
        return integrated_solution

class QualityController:
    """Performs final quality control on the integrated solution."""
    
    def __init__(self, ollama_client, config):
        self.ollama_client = ollama_client
        self.config = config
        self.logger = logging.getLogger("FRA.QualityController")
    
    def validate(self, integrated_solution: Dict[str, Any], processed_problem: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate the integrated solution against the original problem.
        
        Args:
            integrated_solution: The integrated solution
            processed_problem: The original processed problem
            
        Returns:
            Dict containing the validated and potentially improved solution
        """
        self.logger.info("Performing quality control on integrated solution")
        
        # Prepare the validation context
        validation_context = {
            "original_problem": processed_problem,
            "integrated_solution": integrated_solution
        }
        
        instruction = """
        Perform a comprehensive quality check on the integrated solution.
        Verify that:
        1. All original objectives are addressed
        2. All constraints are respected
        3. The solution is internally consistent
        4. The approach is feasible and practical
        5. Any gaps or weaknesses are identified
        
        If improvements are needed, enhance the solution accordingly.
        """
        
        # Use the same format as the integrated solution but add quality metrics
        output_format = dict(integrated_solution)
        output_format["quality_assessment"] = {
            "objectives_addressed": ["How each objective is addressed"],
            "constraints_respected": ["How each constraint is respected"],
            "completeness_score": "Score from 1-10",
            "consistency_score": "Score from 1-10",
            "feasibility_score": "Score from 1-10",
            "identified_gaps": ["Any remaining gaps or issues"],
            "recommendations": ["Final recommendations or improvements"]
        }
        
        validated_solution = self.ollama_client.generate_structured(
            json.dumps(validation_context), instruction, output_format
        )
        
        # Add final validation status
        scores = []
        for score_key in ["completeness_score", "consistency_score", "feasibility_score"]:
            if score_key in validated_solution.get("quality_assessment", {}):
                try:
                    scores.append(float(validated_solution["quality_assessment"][score_key]))
                except (ValueError, TypeError):
                    pass
        
        average_score = sum(scores) / len(scores) if scores else 0
        validated_solution["validation_status"] = "Approved" if average_score >= 7.5 else "Needs Revision"
        
        self.logger.info(f"Quality control completed with status: {validated_solution['validation_status']}")
        return validated_solution