class TaskManager:
    def __init__(self, explorers):
        self.explorers = explorers

    def assign_tasks(self, start, destination):
        candidate_solutions = []
        for explorer in self.explorers:
            solution = explorer.explore(start, destination)
            candidate_solutions.append(solution)
        return candidate_solutions

class PerformanceMonitor:
    def __init__(self):
        self.metrics = []

    def record(self, solution, cost):
        self.metrics.append({'solution': solution, 'cost': cost})

    def evaluate(self):
        if not self.metrics:
            return None
        avg_cost = sum(m['cost'] for m in self.metrics) / len(self.metrics)
        return avg_cost

class FeedbackLoop:
    def __init__(self, explorer_params):
        self.explorer_params = explorer_params

    def adjust_parameters(self, performance_metric):
        if performance_metric is None:
            return
        if performance_metric > 100:
            self.explorer_params['rate'] *= 1.1
        else:
            self.explorer_params['rate'] *= 0.9

class PheromoneRegulator:
    def __init__(self, pheromone_matrix, evaporation_rate=0.1):
        self.pheromone_matrix = pheromone_matrix
        self.evaporation_rate = evaporation_rate

    def evaporate(self):
        keys_to_remove = []
        for edge in list(self.pheromone_matrix.keys()):
            self.pheromone_matrix[edge] *= (1 - self.evaporation_rate)
            if self.pheromone_matrix[edge] < 0.01:
                keys_to_remove.append(edge)
        for edge in keys_to_remove:
            del self.pheromone_matrix[edge]
