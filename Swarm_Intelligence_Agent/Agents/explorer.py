from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

# Gemini API Key (Replace with your actual key)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

class Explorer:
    """
    Uses the Gemini API to generate potential solutions.
    """

    def __init__(self, problem_description, constraints, max_solutions=5):
        self.problem_description = problem_description
        self.constraints = constraints
        self.max_solutions = max_solutions

    def generate_solutions(self):
        """
        Generates potential solutions using the Gemini API.
        """
        prompt = f"I need solutions for the following problem: {self.problem_description}\n"
        prompt += f"Here are the constraints: {self.constraints}\n"
        prompt += "Generate a list of potential solutions, each as a single, concise sentence or phrase. Give me at most {self.max_solutions} solutions."

        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents= prompt
            )
            solutions_text = response.text

            # Basic parsing of the Gemini response (assumes solutions are on separate lines or comma-separated)
            solutions = [s.strip() for s in solutions_text.split("\n") if s.strip()]
            if not solutions:
                solutions = [s.strip() for s in solutions_text.split(",") if s.strip()] #Try comma splitting if newlines don't work

            if not solutions:
                print("Warning: No solutions parsed from Gemini's response.")
                return [] #Return empty if there are no responses

            return solutions
        except Exception as e:
            print(f"Error generating solutions with Gemini API: {e}")
            return []  # Return an empty list in case of an error.

