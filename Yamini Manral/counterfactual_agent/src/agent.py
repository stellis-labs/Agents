# agent.py
import time
from rich.console import Console
from rich.live import Live
from rich.spinner import Spinner
# from rich.panel import Panel
from src.logger import log, log_markdown
from src.config import MAX_SCENARIOS
from src.utils import stream_response
from src.llm_api import call_llm
from rich.markdown import Markdown

console = Console()

class CounterfactualAgent:
    def __init__(self, question):
        self.question = question
        self.scenarios = []
        self.results = []

    def explore_counterfactuals(self):
        """Explore all generated counterfactual scenarios."""
        self.scenarios = self.generate_scenarios(self.question, MAX_SCENARIOS)
        
        for scenario in self.scenarios:
            if scenario.strip():                      
                # log(f"Evaluating scenario: {scenario}")                    
                self.evaluate_scenario(scenario)

                time.sleep(0.5)  
    
    def generate_scenarios(self, question, max_scenarios):
        """Generate counterfactual 'what-if' scenarios for a given question."""
        prompt = f"""
        You are a reasoning agent. The question is:
        {question}

        Generate only a list of {max_scenarios} 'what-if' scenarios to explore alternative outcomes.
        Make a simple list of scenarios, without bullets or numbers. Do not add anything additional. Keep everything precise and concise and to the point.""" 
        # Include logical assumptions and clear hypotheses.
        # DO NOT wander too far from the {question} and keep things hypothetical unless the user inputs specifics.
        # """
        try:
            response = call_llm(prompt)

            full_response = ""
            for chunk in stream_response(response):
                full_response += chunk  # Ensure full text is captured

            full_response = full_response.strip()
            log(f"Scenarios Generated: {full_response}")
            # full_response = stream_response(response).strip()  # Remove leading/trailing whitespace
            scenarios = [s.strip() for s in full_response.split("\n") if s.strip()]  # Remove empty lines
            
            if not scenarios:
                console.print("[bold red]⚠ No scenarios generated![/bold red]")
                return []

            console.print("\n[bold cyan]🧩 Possible Scenarios:[/bold cyan]\n")
            for i, scenario in enumerate(scenarios[:max_scenarios], start=1):
                console.print(f"[bold yellow]{i}. [italic]{scenario}[/italic][/bold yellow]")
            return scenarios
        except Exception as e:
            log(f"Error generating scenarios: {e}", style="bold red")
            return []
        
    # old version    
    def evaluate_scenario(self, scenario):
        with Live(Spinner("dots"), refresh_per_second=10) as live:
            print("\nEvaluating each scenario and generating recommendations...\n")
            """Evaluate the impact of a single scenario."""
            # log(f"Evaluating scenario: {scenario}", style="bold cyan")
            
            prompt = f"""
            You are a reasoning agent. The scenario is:
            {scenario}
            Include logical assumptions and clear hypotheses.
            Use logical reasoning and MCMC simulations to evaluate the impact of each scenario. Provide detailed insights.
            """
            
            try:
                response = call_llm(prompt)
                # live.update(f"Evaluating scenario: {scenario}\n")

                full_response = stream_response(response)
                self.results.append({"scenario": scenario, "evaluation": full_response})

                # Log the evaluation result
                log(f"Scenario Evaluation: {full_response}")

                recommendation = self.generate_recommendation(scenario, full_response)
                self.results[-1]["recommendation"] = recommendation  # Store recommendation in results
                console.print(f"\nEvaluating Scenario: {scenario}\n")
                console.print("\n[bold green]✅ Recommendation:[/bold green]\n")
                console.print(Markdown(f"{recommendation.strip()}"))

                log(f"Recommendation: {recommendation}", style="bold green")

            except Exception as e:
                log(f"Error evaluating scenario: {e}", style="bold red")

    # def summarize_recommendation(self):
    #     """Summarize the evaluations into a final recommendation."""
    #     with Live(Spinner("dots"), refresh_per_second=10) as live:
    #         live.update("Summarizing recommendations and preparing final recommendation...\n")
    #         if not self.results:
    #             return "No valid scenarios were evaluated."

    #         combined_evaluations = "\n".join([result["evaluation"] for result in self.results if isinstance(result, dict) and result.get("evaluation")])

    #         if not combined_evaluations:
    #             return "No valid evaluations available to summarize."

    #         prompt = f"""
    #         You are a reasoning agent. Below are the evaluations of multiple scenarios:
    #         {combined_evaluations}

    #         Summarize the key insights in plain language, and without any calculations included, 
    #         and provide a clear list of actionable recommendation based on the analysis of each scenario. 
    #         """
    #         try:
    #             from src.llm_api import call_llm
    #             response = call_llm(prompt)
    #             return stream_response(response)  
    #         except Exception as e:
    #             log(f"Error summarizing recommendation: {e}", style="bold red")
    #             return "Failed to generate a recommendation."

    def generate_recommendation(self, scenario, evaluation):
        """Generate a recommendation based on a single scenario's evaluation."""

        prompt = f"""
        You are a reasoning agent. Below is the evaluation of a scenario:
        
        Scenario: {scenario}
        Evaluation: {evaluation}

        Based on the evaluation for the {MAX_SCENARIOS} scenarios, provide a concise list of recommendations only. do not add additional text.
        include only recommendations. no key takeaways or conclusions.
        """

        try:
            response = call_llm(prompt)
            return stream_response(response).strip()
        except Exception as e:
            log(f"Error generating recommendation: {e}", style="bold red")
            return "No recommendation available."

    
    def display_final_recommendation(self):
        """Display the final recommendation."""
        recommendation = self.summarize_recommendation()
        log_markdown("Final Recommendation")
        log_markdown(recommendation)
