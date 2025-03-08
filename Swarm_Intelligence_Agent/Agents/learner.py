class Learner:
    """Improves the performance of worker agents over time through learning."""

    def __init__(self):
        self.exploration_strategies = {}  # Store historical data for exploration

    def update_exploration_strategy(self, problem_description, strategy, score):
        if problem_description not in self.exploration_strategies:
            self.exploration_strategies[problem_description] = {}
        self.exploration_strategies[problem_description][strategy] = score

    def get_best_exploration_strategy(self, problem_description):
        if problem_description in self.exploration_strategies:
            return max(self.exploration_strategies[problem_description], key=self.exploration_strategies[problem_description].get)
        return None