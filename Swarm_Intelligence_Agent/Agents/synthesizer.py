from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

# Gemini API Key (Replace with your actual key)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

class Synthesizer:
    """
    Combines the best solutions into a final output.
    """

    def __init__(self, combine_method="best_of_n", n=3):  #can add more sophisticated combinations
        self.combine_method = combine_method
        self.n = n

    def synthesize(self, solutions_with_scores):
        """
        Combines solutions based on the specified method.
        """
        if not solutions_with_scores:
            return "No solutions to synthesize."

        if self.combine_method == "best_of_n":
            # Sort solutions by score in descending order
            sorted_solutions = sorted(solutions_with_scores, key=lambda item: item[1], reverse=True)
            best_solutions = [s[0] for s in sorted_solutions[:self.n]]  # Get the top n solutions
            return "Combined solution: " + ", ".join(best_solutions)  # Combine them into a single string
        else:
            return "Unsupported synthesis method."