from groq import Client
import groq
import os
from dotenv import load_dotenv

load_dotenv()

# GROQ API Key (Replace with your actual key)
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = groq.Client(api_key=GROQ_API_KEY)

class Synthesizer:
    """
    Combines the best solutions into a final output.
    """

    def __init__(self, combine_method="best_of_n", n=1):
        self.combine_method = combine_method
        self.n = n

    def get_reason(self, solutions_with_scores, problem_description, current_time):
        """
        Provides a reason for the chosen solution using the Gemini API.
        """
        try:
            system_prompt = """
            You are a Synthesizer Agent, an AI designed to analyze a problem and explain solutions in a clear, conversational way.
            You have a problem statement and a list of 5 ranked solutions with their scores out of 40.
            Your task is to explain all 5 solutions briefly (1-2 sentences each) as possible options for addressing the problem, like you’re telling someone what can be done.
            Then, conclude by selecting the top-ranked solution (Rank 1) and provide a detailed explanation (4-6 sentences) of why it’s the best, highlighting its strengths, addressing any weaknesses, and showing how it solves the problem effectively.

            Respond ONLY in this format, with no extra text or list-like output:
            Here’s what can be done to address the problem:
            - [Brief explanation of solution 1] 
            - [Brief explanation of solution 2] 
            - [Brief explanation of solution 3] 
            - [Brief explanation of solution 4] 
            - [Brief explanation of solution 5] 

            In conclusion, the best solution is:
            - [Full text of solution 1] 
            - Why it’s best: [Detailed 4-6 sentence explanation of why this is the top choice]
            - Don't mention the score of the solution as the reason. Make it more realistic
            """

            user_prompt = f"""
            Problem Description: {problem_description}
            Ranked Solutions: {solutions_with_scores}
            """

            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )
            reason = response.choices[0].message.content
            return reason
        except Exception as e:
            print(f"Error generating reason with Gemini API: {e}")
            return "Reasoning could not be determined."