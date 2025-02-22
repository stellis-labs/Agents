import random
import math
import osmnx as ox

class Explorer:
    def __init__(self, graph):
        self.graph = graph
        # Pre-calculate node coordinates for efficiency
        self.node_coords = {node: (data.get("y"), data.get("x")) for node, data in graph.nodes(data=True)}

    def euclidean_distance(self, node1, node2):
        """
        Compute an approximate Euclidean distance between two nodes using their (lat, lon) coordinates.
        """
        lat1, lon1 = self.node_coords.get(node1, (None, None))
        lat2, lon2 = self.node_coords.get(node2, (None, None))
        if lat1 is None or lat2 is None:
            return float('inf')
        return math.sqrt((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2)

    def explore(self, start, destination):
        """
        Perform a biased random walk from start to destination.
        Returns a candidate route (list of node IDs) if destination is reached.
        """
        current = start
        path = [current]
        # Increase maximum steps to give the walk more chance to reach the destination
        max_steps = len(self.graph.nodes) * 100  
        steps = 0

        while current != destination and steps < max_steps:
            neighbors = list(self.graph.neighbors(current))
            if not neighbors:
                break

            # Compute Euclidean distances from each neighbor to the destination
            distances = [self.euclidean_distance(n, destination) for n in neighbors]
            # Convert distances into weights (lower distance -> higher weight)
            epsilon = 1e-6  # to avoid division by zero
            weights = [1/(d + epsilon) for d in distances]
            total_weight = sum(weights)
            probabilities = [w / total_weight for w in weights]

            # Choose a neighbor based on the weighted probabilities
            next_node = random.choices(neighbors, weights=probabilities, k=1)[0]
            path.append(next_node)
            current = next_node
            steps += 1

        print(f"Explorer reached node {current} after {steps} steps; Destination: {destination}")
        return path if current == destination else None
