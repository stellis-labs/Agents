import sys
sys.path.append("..")
from .explorer import Explorer
from .evaluator import Evaluator
from .synthesizer import Synthesizer
from .coordinator import Coordinator
from .learner import Learner
from .monitor import Monitor
import datetime

class SwarmIntelligenceAgent:
    def __init__(self, problem_description):
        self.problem_description = problem_description
        self.explorer = Explorer(problem_description)
        self.evaluator = Evaluator(problem_description)
        self.synthesizer = Synthesizer()
        self.coordinator = Coordinator()
        self.learner = Learner()
        self.monitor = Monitor()

    def solve(self):
        """
        Executes the swarm intelligence process.
        """
        solutions = self.explorer.generate_solutions()
        if not solutions:
            return "No viable solutions found during exploration."

        solutions_with_scores = []
        evaluation_time = 0
        for solution in solutions:
            score = self.evaluator.get_evaluation_metrics_and_constraints(solution)
            solutions_with_scores.append((solution, score))
            evaluation_time += 1

        self.monitor.check_for_bottlenecks(len(solutions), evaluation_time)
        feedback = self.monitor.get_feedback()
        if feedback:
            print(f"Monitor feedback: {feedback}")

        current_time = datetime.datetime.now()
        final_solution = self.synthesizer.get_reason(solutions_with_scores, self.problem_description, current_time)
        return final_solution