import os
import json
import requests
import osmnx as ox
from config import GROQ_API_KEY

class GroqLLMInterface:
    def __init__(self):
        # Use the Groq API endpoint (verify this with Groq's docs)
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.api_key = GROQ_API_KEY
        if not self.api_key:
            raise ValueError("Please set your GROQ_API_KEY environment variable.")
        # Groq expects the API key in a Bearer token header and Content-Type as application/json
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def query(self, prompt, messages=None):
        """
        Send a chat completion request to Groq.
        If `messages` is provided, it should be a list of message dicts.
        Otherwise, a single user message is created from the prompt.
        """
        if messages is None:
            messages = [{"role": "user", "content": prompt}]
        payload = {
            "model": "deepseek-r1-distill-llama-70b",
            "messages": messages,
            "temperature": 1,
            "max_completion_tokens": 1024,
            "top_p": 1,
            "stream": False,
            "stop": None,
        }
        response = requests.post(self.api_url, headers=self.headers, json=payload)
        if response.status_code != 200:
            return f"Error: {response.status_code} - {response.text}"
        output = response.json()
        # Expected output: { "choices": [ { "message": { "content": "<text>" } } ] }
        if isinstance(output, dict):
            return output.get("choices", [{}])[0].get("message", {}).get("content", "No text generated.")
        return "No output from Groq API."

    def format_route_response(self, start_location, dest_location, best_route, best_cost, directions):
        prompt = (
            f"Based on the following ACO simulation results, format a human-friendly, step-by-step route recommendation.\n\n"
            f"Start Location: {start_location}\n"
            f"Destination: {dest_location}\n"
            f"Route Directions:\n{directions}\n\n"
            f"Total Distance: {best_cost:.2f} meters\n\n"
            "Please provide clear turn-by-turn directions with street names and landmarks if possible."
        )
        return self.query(prompt)

    def extract_locations(self, query):
        """
        Extract the start and destination from the query using Groq.
        Expects output in valid JSON format exactly as shown:
        {"start": "Boston Logan Airport", "destination": "Northeastern University"}
        """
        prompt = (
            "Extract the start location and destination from the following query. "
            "Return the result in valid JSON format exactly as shown below:\n"
            '{"start": "Boston Logan Airport", "destination": "Northeastern University"}\n'
            f"Query: {query}\n"
            "Output:"
        )
        result = self.query(prompt)
        print("LLM raw output length:", len(result))
        print("LLM raw output:", result)  # Debug line

        # Use a regular expression to capture the first JSON block
        import re
        match = re.search(r'({.*?})', result, re.DOTALL)
        if match:
            json_str = match.group(1)
            print("Extracted JSON substring:", json_str)
            try:
                data = json.loads(json_str)
                start = data.get("start")
                dest = data.get("destination")
                if start and dest:
                    print("Successfully extracted start and destination.")
                    return start, dest
                else:
                    print("Parsed JSON but missing keys: start or destination.")
            except Exception as e:
                print("JSON parsing failed for substring:", json_str)
                print("Exception:", e)
        else:
            print("No JSON substring found in the LLM output.")
        
        # Fallback extraction if regex fails.
        start = None
        dest = None
        for part in result.split(";"):
            if "start:" in part.lower():
                start = part.split(":")[1].strip()
            elif "destination:" in part.lower():
                dest = part.split(":")[1].strip()
        if start and dest:
            print("Fallback extraction succeeded:", start, dest)
        else:
            print("Fallback extraction failed.")
        return start, dest


class LLMInterface:
    def __init__(self):
        self.llm = GroqLLMInterface()

    def query(self, query):
        # Extract start and destination using Groq.
        start_location, dest_location = self.llm.extract_locations(query)
        if not start_location or not dest_location:
            return "Could not extract start and destination from the query."
        
        # Import geocoding and directions functions.
        from utils.geocoding import geocode_location, get_graph_for_route
        from utils.directions import generate_directions
        
        # Geocode the locations.
        start_coords = geocode_location(start_location)
        dest_coords = geocode_location(dest_location)
        if not start_coords or not dest_coords:
            return "Could not geocode one or both locations."
        
        # Retrieve the road network graph.
        graph = get_graph_for_route(start_coords, dest_coords)
        # Map coordinates to nearest graph nodes.
        start_node = ox.distance.nearest_nodes(graph, start_coords[1], start_coords[0])
        dest_node  = ox.distance.nearest_nodes(graph, dest_coords[1], dest_coords[0])

        # --- Sanity Check: Try computing a shortest path directly ---
        import networkx as nx
        try:
            sp = nx.shortest_path(graph, source=start_node, target=dest_node, weight='length')
            print("Shortest path found:", sp)
        except Exception as e:
            print("No route exists between start and destination:", e)
        # --- End Sanity Check ---
        
        # Import ACO simulation functions.
        from aco_agents.explorer import Explorer
        from aco_agents.trailblazer import Trailblazer
        from aco_agents.exploiter import Exploiter
        from aco_agents.helper_agents import TaskManager, PerformanceMonitor, FeedbackLoop, PheromoneRegulator
        
        # Run the ACO simulation.
        best_route, best_cost = simulate_ACO(graph, start_node, dest_node)
        if best_route is None:
            return "Could not determine a route."
        
        # Generate human-friendly directions using street names.
        directions = generate_directions(graph, best_route)
        # Use Groq to polish the output.
        response = self.llm.format_route_response(
            start_location, dest_location, best_route, best_cost, directions)
        return response

# Import the ACO simulation function to avoid circular dependencies.
from aco_agents.helper_agents import *
from aco_agents.explorer import Explorer
from aco_agents.trailblazer import Trailblazer
from aco_agents.exploiter import Exploiter
from aco_agents.helper_agents import TaskManager, PerformanceMonitor, FeedbackLoop, PheromoneRegulator

def simulate_ACO(graph, start_node, dest_node):
    pheromone_matrix = {}
    explorers = [Explorer(graph) for _ in range(5)]
    trailblazers = [Trailblazer(pheromone_matrix, graph) for _ in range(5)]
    exploiters = [Exploiter(graph, pheromone_matrix) for _ in range(3)]
    
    task_manager = TaskManager(explorers)
    performance_monitor = PerformanceMonitor()
    explorer_params = {'rate': 1.0}
    feedback_loop = FeedbackLoop(explorer_params)
    pheromone_regulator = PheromoneRegulator(pheromone_matrix, evaporation_rate=0.1)
    
    # Get candidate solutions using random walks from explorers
    candidate_solutions = task_manager.assign_tasks(start_node, dest_node)
    print("Candidate solutions:")
    for i, sol in enumerate(candidate_solutions):
        print(f"Candidate {i+1}: {sol}")
    
    refined_solutions = []
    for i, (solution, trailblazer) in enumerate(zip(candidate_solutions, trailblazers)):
        if solution is None:
            print(f"Candidate {i+1} did not reach the destination.")
            continue
        quality, cost = trailblazer.evaluate_solution(solution)
        print(f"Candidate {i+1} evaluated: quality={quality}, cost={cost}")
        trailblazer.deposit_pheromones(solution, quality)
        refined = exploiters[0].refine_solution(solution)
        print(f"Candidate {i+1} refined solution: {refined}")
        if refined is None:
            print(f"Candidate {i+1} could not be refined further.")
            continue
        refined_cost = Exploiter(graph, pheromone_matrix).route_cost(refined)
        print(f"Candidate {i+1} refined cost: {refined_cost}")
        performance_monitor.record(refined, refined_cost)
        refined_solutions.append((refined, refined_cost))
    
    print("Refined solutions:", refined_solutions)
    avg_cost = performance_monitor.evaluate()
    print("Average cost:", avg_cost)
    feedback_loop.adjust_parameters(avg_cost)
    pheromone_regulator.evaporate()
    
    if not refined_solutions:
        print("No refined solutions found.")
        return None, float('inf')
    best_route, best_cost = min(refined_solutions, key=lambda x: x[1])
    print("Best route found with cost:", best_cost)
    return best_route, best_cost