import sys
sys.path.append("..")
from .explorer import Explorer
from .evaluator import Evaluator
from .synthesizer import Synthesizer

class SwarmIntelligenceAgent:
    def __init__(self, problem_description, constraints):
        self.problem_description = problem_description
        self.constraints = constraints
        self.explorer = Explorer(problem_description, constraints)
        self.evaluator = Evaluator(problem_description, constraints)
        self.synthesizer = Synthesizer()

    def solve(self):
        """
        Executes the swarm intelligence process.
        """
        # 1. Exploration
        solutions = self.explorer.generate_solutions()

        if not solutions:
            return "No viable solutions found during exploration."

        # 2. Evaluation
        solutions_with_scores = []
        for solution in solutions:
            score = self.evaluator.evaluate_solution(solution)
            solutions_with_scores.append((solution, score))

        # 3. Synthesis
        final_solution = self.synthesizer.synthesize(solutions_with_scores)

        # **Improved Output Formatting**
        formatted_solutions = "\n".join(f"{i+1}. {sol[0]}" for i, sol in enumerate(solutions_with_scores))

        return f"Recommended Solutions:\n{formatted_solutions}\n\nFinal Optimized Choice:\n{final_solution}"