from google import genai

# Gemini API Key (Replace with your actual key)
GEMINI_API_KEY = "AIzaSyC_ruWIn55pe3F8hPO4dEecsTEQ3JVMHL4"
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


# Main Swarm Intelligence Agent
class SwarmIntelligenceAgent:
    def __init__(self, problem_description, constraints):
        self.problem_description = problem_description
        self.constraints = constraints
        self.explorer = Explorer(problem_description, constraints)
        self.evaluator = Evaluator(problem_description, constraints)
        self.synthesizer = Synthesizer()

    def solve(self):
        """
        Executes the swarm intelligence process.
        """
        # 1. Exploration
        solutions = self.explorer.generate_solutions()

        if not solutions:
            return "No viable solutions found during exploration."

        # 2. Evaluation
        solutions_with_scores = []
        for solution in solutions:
            score = self.evaluator.evaluate_solution(solution)
            solutions_with_scores.append((solution, score))

        # 3. Synthesis
        final_solution = self.synthesizer.synthesize(solutions_with_scores)

        # **Improved Output Formatting**
        formatted_solutions = "\n".join(f"{i+1}. {sol[0]}" for i, sol in enumerate(solutions_with_scores))

        return f"Recommended Solutions:\n{formatted_solutions}\n\nFinal Optimized Choice:\n{final_solution}"




# Example Usage
if __name__ == "__main__":
    problem_description = "Optimize better way to travel from Boston to Newyork City"
    constraints = "Must be cost-effective and relatively quick."

    agent = SwarmIntelligenceAgent(problem_description, constraints)
    final_solution = agent.solve()

    print("Final Solution:", final_solution)