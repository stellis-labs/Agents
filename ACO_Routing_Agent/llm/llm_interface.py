import os
import json
import requests
import re
import osmnx as ox
from config import GROQ_API_KEY

def remove_think_blocks(text):
    """
    Removes any <think>...</think> content from the text.
    """
    return re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)

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
        {"start": "", "destination": ""}
        """
        prompt = (
            "Extract the start location and destination from the following query. "
            "Return the result in valid JSON format exactly as shown below:\n"
            '{"start": "", "destination": ""}\n'
            f"Query: {query}\n"
            "Output:"
        )
        result = self.query(prompt)

        # Remove <think> blocks right away so they're not printed in debug
        result = remove_think_blocks(result)

        print("LLM raw output length:", len(result))
        print("LLM raw output:", result)  # Debug line without <think>

        match = re.search(r'({.*?})', result, re.DOTALL)
        if match:
            json_str = match.group(1)
            print("Extracted JSON substring:", json_str)
            try:
                data = json.loads(json_str)
                start_llm = data.get("start")
                dest_llm = data.get("destination")
                if start_llm and dest_llm:
                    print("LLM extracted:", start_llm, "to", dest_llm)
                    # Validate they appear in the user query
                    if self._locations_consistent_with_query(start_llm, dest_llm, query):
                        print("LLM extraction is consistent with user query.")
                        return start_llm, dest_llm
                    else:
                        print("LLM extraction is NOT consistent with user query. Falling back.")
                else:
                    print("LLM JSON missing 'start' or 'destination'. Falling back.")
            except Exception as e:
                print("JSON parsing failed:", e)
        else:
            print("No JSON substring found in the LLM output. Falling back.")

        # Fallback approach
        print("Attempting fallback parse from user query...")
        start_fb, dest_fb = self._fallback_parse(query)
        if start_fb and dest_fb:
            print("Fallback parse succeeded:", start_fb, dest_fb)
            return start_fb, dest_fb
        else:
            print("Fallback parse failed.")
            return None, None
        
    def _fallback_parse(self, query):
        """
        A naive fallback that looks for the words 'from' and 'to' in the user query.
        Example: 'give me the shortest path from X to Y'
        """
        query_lower = query.lower()
        start_val, dest_val = None, None
        if "from" in query_lower and "to" in query_lower:
            try:
                after_from = query_lower.split("from")[1]
                parts = after_from.split("to")
                start_val = parts[0].strip().title()
                dest_val = parts[1].strip().title()
            except Exception as e:
                print("Fallback parse error:", e)
        return start_val, dest_val

    def _locations_consistent_with_query(self, start_llm, dest_llm, user_query):
        """
        A simple check to see if the LLM's extracted start/destination 
        at least appear in the user's query. Adjust as needed.
        """
        q_lower = user_query.lower()
        return (start_llm.lower() in q_lower) and (dest_llm.lower() in q_lower)

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
        response = self.llm.format_route_response(start_location, dest_location, best_route, best_cost, directions)
        
        # Remove <think> blocks from the final LLM response
        response = remove_think_blocks(response)
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
    
    # ---------------------------
    # Gather solutions that reached the destination
    # and sort them by route length (fewest steps first).
    # ---------------------------
    reached_solutions = []
    for i, sol in enumerate(candidate_solutions):
        if sol is not None:
            # (agent_index, route_list)
            reached_solutions.append((i, sol))
    
    if not reached_solutions:
        print("No solutions reached the destination.")
        return None, float('inf')
    
    # Sort solutions by the number of steps in the route
    reached_solutions.sort(key=lambda x: len(x[1]))
    
    # Pick only the best two (fewest steps)
    top_solutions = reached_solutions[:2]
    print("Evaluating only these top solutions (fewest steps):")
    for idx, (agent_idx, route) in enumerate(top_solutions, start=1):
        print(f"Top {idx} => Explorer {agent_idx+1}, steps={len(route)}: {route}")
    
    # Evaluate & refine only these top solutions
    refined_solutions = []
    for agent_idx, route in top_solutions:
        # Evaluate using the matching trailblazer
        quality, cost = trailblazers[agent_idx].evaluate_solution(route)
        print(f"Explorer {agent_idx+1} route cost={cost}, quality={quality}")
        
        # Deposit pheromones
        trailblazers[agent_idx].deposit_pheromones(route, quality)
        
        # Refine solution using Exploiter 0 (or pick any exploiter)
        refined = exploiters[0].refine_solution(route)
        print(f"Refined solution (Explorer {agent_idx+1}): {refined}")
        
        if refined is None:
            print(f"Explorer {agent_idx+1} route could not be refined.")
            continue
        
        refined_cost = exploiters[0].route_cost(refined)
        print(f"Refined cost (Explorer {agent_idx+1}): {refined_cost}")
        performance_monitor.record(refined, refined_cost)
        refined_solutions.append((refined, refined_cost))
    
    # If no solutions remain after refining
    if not refined_solutions:
        print("No refined solutions found among top routes.")
        return None, float('inf')
    
    # Perform feedback & pheromone evaporation
    avg_cost = performance_monitor.evaluate()
    print("Average cost among top routes:", avg_cost)
    feedback_loop.adjust_parameters(avg_cost)
    pheromone_regulator.evaporate()
    
    # Pick the best among the refined solutions
    best_route, best_cost = min(refined_solutions, key=lambda x: x[1])
    print("Best route found with cost:", best_cost)
    return best_route, best_cost

