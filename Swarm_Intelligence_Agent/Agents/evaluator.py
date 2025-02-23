from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

# Gemini API Key (Replace with your actual key)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

class Evaluator:
    """
    Evaluates the quality of solutions based on metrics determined by Gemini.
    """

    def __init__(self, problem_description, constraints):
       self.problem_description = problem_description
       self.constraints = constraints

    def get_evaluation_metrics(self, solution):
        """
        Asks Gemini to suggest evaluation metrics for the solution.
        """

        prompt = f"Based on the problem description: {self.problem_description}, constraints: {self.constraints}, and the following potential solution: '{solution}', what are the most important evaluation metrics to consider? Provide the metrics as a comma-separated list of key phrases."

        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents= prompt
            )
            metrics_text = response.text.strip()
            metrics = [m.strip() for m in metrics_text.split(",")]
            return metrics
        except Exception as e:
            print(f"Error getting evaluation metrics from Gemini API: {e}")
            return []

    def evaluate_solution(self, solution):
        """
        Evaluates a single solution and returns a score (higher is better).
        """

        metrics = self.get_evaluation_metrics(solution) #Get metrics specific for THIS solution

        if not metrics:
            print(f"Warning: No metrics found for solution: '{solution}'")
            return 0

        score = 0
        for metric in metrics:
            # VERY simple example: award points for keywords matching the metrics
            if metric.lower() in solution.lower():
                score += 1  # Simple keyword matching
        return score