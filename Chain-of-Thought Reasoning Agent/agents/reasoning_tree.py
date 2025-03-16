from agents.sub_agent import SubAgent

class ReasoningTreeNode:
    def __init__(self, problem: str, llm, depth: int = 0, max_depth: int = 6):
        """
        Represents a node in the reasoning tree.
        :param problem: The question assigned to this node.
        :param llm: LLM client for processing.
        :param depth: Current depth of the reasoning process.
        :param max_depth: Maximum depth allowed for the reasoning tree.
        """
        self.problem = problem
        self.llm = llm
        self.children = []
        self.response = None
        self.depth = depth
        self.max_depth = max_depth
        self.sub_agent = SubAgent(self.llm)
        self.step_function = self.get_step_function()

    def get_step_function(self):
        """
        Determines which function to call based on the depth level.
        """
        step_functions = [
            self.sub_agent.identify_key_components,
            self.sub_agent.generate_questions,
            self.sub_agent.generate_hypotheses,
            self.sub_agent.evaluate_hypothesis,
            self.sub_agent.generate_solutions,
            self.sub_agent.evaluate_solutions_with_history,
            self.sub_agent.consolidate_final_recommendation,
        ]
        return step_functions[min(self.depth, len(step_functions) - 1)]

    def expand(self):
        if self.depth >= self.max_depth:
            return  

        step_output = self.step_function(self.problem)  # Get structured response for this step
        self.response = step_output  

        # Set different limits for each step
        sub_agent_limit = {
            1: 6,  # Max 5-6 key components (allows full problem breakdown)
            2: 2,  # Max 2 sub-questions per key component
            3: 2,  # Max 2 hypotheses per question
            4: 1,  # Max 1 evaluation per hypothesis
            5: 1,  # Max 1 solution per evaluation
            6: 2,  # Max 2 historical evaluations per solution
        }
        
        max_sub_agents = sub_agent_limit.get(self.depth, 1)  # Default to 1 if not specified
        selected_outputs = step_output[:max_sub_agents]  # Restrict expansion to the required count

        for sub_item in selected_outputs:  
            sub_node = ReasoningTreeNode(sub_item, self.llm, self.depth + 1, self.max_depth)
            sub_node.expand()
            self.children.append(sub_node)


    def get_final_output(self):
        """
        Recursively gathers and consolidates responses from all child nodes.
        """
        final_output = [f"[Step {self.depth + 1}] {self.problem}"]
        final_output.extend(self.response)

        for child in self.children:
            final_output.extend(child.get_final_output())  # Ensure all child outputs are included

        return final_output
