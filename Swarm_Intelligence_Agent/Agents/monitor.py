import random
import datetime

class Monitor:
    """Tracks the performance of worker agents and provides real-time feedback."""

    def __init__(self):
        self.bottlenecks = []

    def check_for_bottlenecks(self, solutions_count, evaluation_time):
        if solutions_count > 10 and evaluation_time > 5:
            self.bottlenecks.append("Evaluator is overloaded.")
        # Add more checks as needed

    def get_feedback(self):
        return self.bottlenecks