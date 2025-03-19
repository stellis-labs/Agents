import json5
import json
import logging
from typing import Dict, Any
from agents.explorer import ExplorerAgent
from agents.trailblazer import TrailblazerAgent
from agents.exploiter import ExploiterAgent

class ACOLLMAgent:
    """
    The ACOLLMAgent orchestrates the optimization process using only the basic worker agents:
      - Explorer: generates candidate solutions.
      - Trailblazer: evaluates the candidates with pheromone annotations.
      - Exploiter: refines the evaluated candidates.
    """
    def __init__(self, api_key: str, constraints: str, max_solutions: int = 5, model: str = "deepseek-r1-distill-llama-70b"):
        self.api_key = api_key
        self.model = model
        self.constraints = constraints
        self.max_solutions = max_solutions
        
        # Instantiate basic worker agents
        self.explorer = ExplorerAgent(api_key, model, constraints, max_solutions)
        self.trailblazer = TrailblazerAgent(api_key, model)
        self.exploiter = ExploiterAgent(api_key, model)
        
        # Problem details
        self.problem_definition: str = ""
        self.problem_analysis: Dict[str, Any] = {}
    
    def initialize(self, problem_definition: str) -> None:
        self.problem_definition = problem_definition
        # For simplicity, we simply store the problem definition as analysis.
        self.problem_analysis = {"problem": problem_definition}
        logging.info(f"Problem analysis: {self.problem_analysis}")
    
    def optimize(self) -> Dict[str, Any]:
        step_details = {}
        
        # Step 1: Explorer generates candidate solutions.
        try:
            candidates = self.explorer.explore(self.problem_definition, self.max_solutions)
            step_details["explorer"] = [f"Explorer generated: {cand['candidate']}" for cand in candidates]
        except Exception as e:
            logging.error(f"Error during Explorer phase: {e}")
            raise
        
        # Step 2: Trailblazer evaluates candidates.
        try:
            evaluated = self.trailblazer.evaluate(candidates)
            step_details["trailblazer"] = [
                f"Trailblazer evaluated: {item['candidate']} with label {item.get('pheromone_label', 'unknown')}"
                for item in evaluated
            ]
        except Exception as e:
            logging.error(f"Error during Trailblazer phase: {e}")
            raise
        
        # Step 3: Exploiter refines evaluated candidates.
        try:
            refined = self.exploiter.refine(evaluated)
            step_details["exploiter"] = [
                f"Exploiter refined: {item['candidate']} to score {item.get('refined_score', 0)}"
                for item in refined
            ]
        except Exception as e:
            logging.error(f"Error during Exploiter phase: {e}")
            raise
        
        # Choose best solution based on refined_score.
        try:
            best_solution = max(refined, key=lambda x: x.get("refined_score", 0))
        except Exception as e:
            logging.error(f"Error choosing best solution: {e}")
            raise
        
        formatted_output = (
            "Agent Output:\n"
            "Step 1: Explorer generated candidates:\n" + "\n".join(step_details.get("explorer", [])) + "\n\n" +
            "Step 2: Trailblazer evaluated candidates:\n" + "\n".join(step_details.get("trailblazer", [])) + "\n\n" +
            "Step 3: Exploiter refined candidates:\n" + "\n".join(step_details.get("exploiter", [])) + "\n\n" +
            f"Final Recommendation: Use {best_solution['candidate']} with a refined score of {best_solution.get('refined_score', 0)}."
        )
        results = {
            "best_solution": best_solution,
            "step_details": step_details,
            "formatted_output": formatted_output,
            "raw_candidates": candidates,
            "raw_evaluated": evaluated,
            "raw_refined": refined
        }
        logging.info("Final Recommendation:")
        logging.info(formatted_output)
        return results
    
    def save_results(self, filename: str) -> None:
        results = {
            "problem_definition": self.problem_definition,
            "problem_analysis": self.problem_analysis,
            "best_solution": self.optimize()["best_solution"]
        }
        with open(filename, 'w', encoding="utf-8") as f:
            json5.dump(results, f, indent=2)
        logging.info(f"Results saved to {filename}")
