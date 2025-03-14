from agents.reasoning_tree import ReasoningTreeNode
from utils.display_manager import DisplayManager

class ReasoningAgent:
    def __init__(self, llm):
        self.llm = llm
        self.display = DisplayManager()

    def solve_problem(self, problem: str):
        """ Initiates the reasoning process using the LLM """
        self.display.display_problem(problem)

        # Create root node and expand the reasoning tree
        root_node = ReasoningTreeNode(problem, self.llm)
        root_node.expand()

        # Retrieve and display the final output
        final_response = root_node.get_final_output()
        self.display.display_step("Final Recommendation", final_response)