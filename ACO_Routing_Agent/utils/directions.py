def generate_directions(graph, route):
    """
    Convert a route (list of node IDs) into step-by-step directions using street names and distances.
    Aggregates consecutive segments on the same road.
    """
    if route is None or len(route) < 2:
        return "No valid route found."
    
    directions = []
    current_road = None
    segment_distance = 0
    
    for i in range(len(route) - 1):
        u = route[i]
        v = route[i+1]
        edge_data = graph.get_edge_data(u, v)
        if not edge_data:
            continue
        # Choose the first available edge if multiple exist.
        edge = edge_data[list(edge_data.keys())[0]]
        road_name = edge.get("name", "Unnamed Road")
        distance = edge.get("length", 0)
        
        if current_road is None:
            current_road = road_name
            segment_distance = distance
        elif road_name == current_road:
            segment_distance += distance
        else:
            directions.append(f"Take {current_road} for {segment_distance:.0f} meters.")
            current_road = road_name
            segment_distance = distance
        
        if i == len(route) - 2:
            directions.append(f"Then take {current_road} for {segment_distance:.0f} meters to reach your destination.")
    
    return "\n".join(directions)
