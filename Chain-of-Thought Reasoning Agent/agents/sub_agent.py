class SubAgent:
    def __init__(self, llm):
        self.llm = llm

    def identify_key_components(self, problem: str) -> list:
        prompt = f"Break down the following problem into at most 6 key components:\n\n{problem}"
        response = self.llm.run(prompt)
        return response.split("\n")[:6]  # Limit to 5-6 key components

    def generate_questions(self, key_component: str) -> list:
        prompt = f"Generate 1-2 key questions based on this key component:\n\n{key_component}"
        response = self.llm.run(prompt)
        return response.split("\n")[:2]  # Limit to 2 questions

    def generate_hypotheses(self, question: str) -> list:
        prompt = f"Provide 1-2 hypotheses for this question:\n\n{question}"
        response = self.llm.run(prompt)
        return response.split("\n")[:2]  # Limit to 2 hypotheses

    def evaluate_hypothesis(self, hypothesis: str) -> list:
        prompt = f"Evaluate the following hypothesis concisely:\n\n{hypothesis}"
        response = self.llm.run(prompt)
        return [response]  # Only 1 evaluation per hypothesis

    def generate_solutions(self, evaluation: str) -> list:
        prompt = f"Suggest 1-2 solutions based on this evaluation:\n\n{evaluation}"
        response = self.llm.run(prompt)
        return response.split("\n")[:2]  # Limit to 2 solutions

    def evaluate_solutions_with_history(self, solution: str) -> list:
        prompt = f"Evaluate this solution using historical data:\n\n{solution}"
        response = self.llm.run(prompt)
        return [response]  # Only 1 evaluation per solution

    def consolidate_final_recommendation(self, historical_outcomes: list) -> list:
        prompt = (
            "Based on all historical evaluations, provide a final recommendation in concise bullet points:\n\n"
            f"{historical_outcomes}"
        )
        response = self.llm.run(prompt)
        return response.split("\n")[:3]  # Ensure concise final recommendations
