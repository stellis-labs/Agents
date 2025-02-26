class Trailblazer:
    def __init__(self, pheromone_matrix, graph):
        self.pheromone_matrix = pheromone_matrix
        self.graph = graph

    def evaluate_solution(self, solution):
        """
        Calculate the total route cost and compute its quality as inverse cost.
        """
        if solution is None:
            return 0, float('inf')
        total_cost = 0
        for i in range(len(solution) - 1):
            edge_data = self.graph.get_edge_data(solution[i], solution[i+1])
            if edge_data is None:
                return 0, float('inf')
            cost = edge_data[0]['length']  # use first edge if multiple exist
            total_cost += cost
        quality = 1 / total_cost if total_cost > 0 else 0
        return quality, total_cost

    def deposit_pheromones(self, solution, quality):
        """
        Increase pheromone levels along the route edges.
        """
        if solution is None:
            return
        for i in range(len(solution) - 1):
            edge = (solution[i], solution[i+1])
            self.pheromone_matrix[edge] = self.pheromone_matrix.get(edge, 0) + quality
