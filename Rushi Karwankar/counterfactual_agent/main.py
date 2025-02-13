from src.config import Config
from src.logger import Logger
from src.llm_client import LLMClient
from src.analyzer import ProblemAnalyzer
from src.evaluation import HypothesisEvaluator
from src.simulation import OutcomeSimulator


class CounterfactualReasoningSystem:
    def __init__(self):
        self.logger = Logger()
        self.llm_client = LLMClient(Config.OLLAMA_API_URL, self.logger)
        self.analyzer = ProblemAnalyzer(self.llm_client, self.logger)
        self.evaluator = HypothesisEvaluator(Config.EVALUATION_WEIGHTS)
        self.simulator = OutcomeSimulator(Config.SIMULATION_PARAMS)
        
    def provide_insights(self, evaluations, outcomes):
        combined_scores = []
        for ((hyp1, eval_score), (_, sim_score)) in zip(evaluations, outcomes):
            combined_score = (eval_score + sim_score) / 2
            combined_scores.append((hyp1, combined_score))
        
        top_recommendations = sorted(combined_scores, key=lambda x: x[1], reverse=True)[:2]
        
        recommendations_text = "### Final Recommendations:\n\n"
        for i, (hypothesis, _) in enumerate(top_recommendations, 1):
            recommendations_text += f"{i}. {hypothesis}\n"
        
        self.logger.log_markdown(recommendations_text)

    def solve(self, problem):
        self.logger.log_markdown(f"## Analyzing problem: {problem}")

        # Step 1: Identify components
        components = self.analyzer.identify_components(problem)
        if components:
            self.logger.log_markdown(f"### Key Components:\n{', '.join(components)}")

        # Step 2: Generate hypotheses
        hypotheses = self.analyzer.generate_hypotheses(problem)

        # Step 3: Evaluate hypotheses
        evaluations = self.evaluator.evaluate_hypotheses(hypotheses)

        # Step 4: Simulate outcomes
        outcomes = self.simulator.simulate_outcomes(hypotheses)

        # Step 5: Provide insights
        self.provide_insights(evaluations, outcomes)

if __name__ == "__main__":
    system = CounterfactualReasoningSystem()
    problem_statement = "How to optimize the supply chain to reduce costs and improve efficiency?"
    system.solve(problem_statement)