import os
from dotenv import load_dotenv
from groq import Client
import groq

load_dotenv()

# GROQ API Key (Replace with your actual key)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = groq.Client(api_key=GROQ_API_KEY)

class Explorer:
    """
    Uses the Gemini API to generate potential solutions.
    """

    def __init__(self, problem_description, max_solutions=5):
        self.problem_description = problem_description
        self.max_solutions = max_solutions

    def generate_solutions(self):

        prompt = """
        You are an Explorer Agent, an AI designed to provide creative and practical solutions to problems.
        Your task is to take the following problem statement and generate exactly 5 distinct possible solutions.
        Each solution should be concise (2-3 sentences), actionable, and relevant to the problem.
        Avoid overly vague or repetitive ideas.
        Focus on diversity of approaches and clarity.

        Return your response as a JSON list of 5 solutions in the following format, with no additional text, comments, or formatting outside the list:
        [
            "Description of solution 1",
            "Description of solution 2",
            "Description of solution 3",
            "Description of solution 4",
            "Description of solution 5"
        ]
        """

        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": self.problem_description}
                ]
            )
            # print("response", response.choices[0].message.content)
            solutions_text = response.choices[0].message.content
            solutions = solutions_text.split('",')
            return solutions

        except Exception as e:
            print(f"Error generating solutions with Gemini API: {e}")
            return {}