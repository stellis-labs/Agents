# agent.py
import time
from rich.live import Live
from rich.spinner import Spinner
from logger import log, log_markdown
from scenario import generate_scenarios, evaluate_scenario
from config import MAX_SCENARIOS
from utils import stream_response

class CounterfactualAgent:
    def __init__(self, question):
        self.question = question
        self.scenarios = []
        self.results = []

    def explore_counterfactuals(self):
        """Explore all generated counterfactual scenarios."""
        self.scenarios = generate_scenarios(self.question, MAX_SCENARIOS)

        with Live(Spinner("dots"), refresh_per_second=15) as live:
            live.update("Generating scenarios...")
            for i, scenario in enumerate(self.scenarios):
                if scenario.strip():
                    live.update(f"Evaluating scenario {i + 1}/{len(self.scenarios)}: {scenario}")
                    self.results.append(evaluate_scenario(scenario))

    def summarize_recommendation(self):
        """Summarize the evaluations into a final recommendation."""
        if not self.results:
            return "No valid scenarios were evaluated."

        combined_evaluations = "\n".join([result["evaluation"] for result in self.results])
        prompt = f"""
        You are a reasoning agent. Below are the evaluations of multiple scenarios:
        {combined_evaluations}

        Summarize the key insights and provide a clear, actionable recommendation based on the analysis.
        """
        try:
            from llm_api import call_llm
            response = call_llm(prompt)
            return stream_response(response)
        except Exception as e:
            log(f"Error summarizing recommendation: {e}", style="bold red")
            return "Failed to generate a recommendation."

    def display_final_recommendation(self):
        """Display the final recommendation."""
        recommendation = self.summarize_recommendation()
        log_markdown("# Final Recommendation")
        log_markdown(recommendation)
