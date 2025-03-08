class Coordinator:
    """Manages communication and resource allocation among worker agents."""

    def __init__(self):
        self.resources = {"explorer": 1, "evaluator": 1, "synthesizer": 1}

    def allocate_resources(self, agent_type, amount):
        if self.resources[agent_type] >= amount:
            self.resources[agent_type] -= amount
            return True
        return False

    def release_resources(self, agent_type, amount):
        self.resources[agent_type] += amount