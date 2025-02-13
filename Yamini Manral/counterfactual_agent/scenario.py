# scenario.py
from llm_api import call_llm
from utils import stream_response
from logger import log

def generate_scenarios(question, max_scenarios):
    """Generate counterfactual 'what-if' scenarios for a given question."""
    prompt = f"""
    You are a reasoning agent. The question is:
    {question}

    Generate a list of {max_scenarios} 'what-if' scenarios to explore alternative outcomes. 
    Include logical assumptions and clear hypotheses.
    """

    try:
        response = call_llm(prompt)
        full_response = stream_response(response)
        return full_response.split("\n")[:max_scenarios]
    except Exception as e:
        log(f"Error generating scenarios: {e}", style="bold red")
        return []

def evaluate_scenario(scenario):
    """Evaluate the impact of a single scenario."""
    prompt = f"""
    You are a reasoning agent. The scenario is:
    {scenario}

    Use logical reasoning and probabilistic models to evaluate the impact of this scenario. Provide detailed insights.
    """
    
    try:
        response = call_llm(prompt)
        full_response = stream_response(response)
        return {"scenario": scenario, "evaluation": full_response}
    except Exception as e:
        log(f"Error evaluating scenario: {e}", style="bold red")
        return {"scenario": scenario, "evaluation": "Evaluation failed."}
