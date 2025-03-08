import os
from dotenv import load_dotenv
from groq import Client
import groq

load_dotenv()

# GROQ API Key (Replace with your actual key)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = groq.Client(api_key=GROQ_API_KEY)

class Evaluator:
    def __init__(self, problem_description):
        self.problem_description = problem_description

    def get_evaluation_metrics_and_constraints(self, solution):
        system_prompt = """
        You are an Evaluator Agent, an AI designed to assess solutions to a problem based on feasibility, cost-effectiveness, impact, and scalability.
        Your task is to evaluate the following problem statement and the single solution provided below.
        Score the solution out of 10 for each factor (feasibility, cost-effectiveness, impact, scalability), then calculate the total score out of 40.
        Do not include individual scores or explanations, only the final total score.

        Provide your response as a single integer representing the total score out of 40, with no additional text or formatting:
        28
        """

        user_prompt = f"""
        Problem_description: {self.problem_description}
        Solutions: {solution}
        """

        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            score = response.choices[0].message.content
            return score
        except Exception as e:
            print(f"Error getting evaluation metrics and constraints from Gemini API: {e}")
            return []