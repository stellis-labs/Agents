import argparse
import json
import logging
import os
from fra_system import FRAgent

def setup_logging():
    """Configure logging for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler("fra_logs.log"),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger("FRA")

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description='Fractal Reasoning Agent (FRA)')
    parser.add_argument('--problem', type=str, help='Problem statement to solve')
    parser.add_argument('--config', type=str, default='config/default_config.json',
                         help='Path to configuration file')
    parser.add_argument('--output', type=str, default='output/solution.json',
                        help='Path to save the output')
    return parser.parse_args()

def load_config(config_path):
    """Load configuration from JSON file."""
    try:
        with open(config_path, 'r') as file:
            return json.load(file)
    except Exception as e:
        logger.error(f"Error loading configuration: {e}")
        raise

def ensure_output_directory(output_path):
    """Ensure the output directory exists."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

def main():
    # Setup logging
    global logger
    logger = setup_logging()
    
    # Parse arguments
    args = parse_arguments()
    
    # Get problem statement from arguments or prompt user
    problem_statement = args.problem
    if not problem_statement:
        problem_statement = input("Please enter your complex problem statement: ")
    
    # Load configuration
    config = load_config(args.config)
    
    # Ensure output directory exists
    ensure_output_directory(args.output)
    
    # Initialize and run the Fractal Reasoning Agent
    fra = FRAgent(config)
    solution = fra.solve(problem_statement)
    
    # Save the solution
    with open(args.output, 'w') as file:
        json.dump(solution, file, indent=2)
    
    logger.info(f"Solution saved to {args.output}")
    
    # Print a summary of the solution
    print("\n===== Fractal Reasoning Agent Solution =====")
    print(f"Problem: {problem_statement}")
    print("\nSummary:")
    
    # Fix: Check if 'summary' key exists in solution dictionary
    if 'summary' in solution:
        print(solution['summary'])
    else:
        # Either generate a summary from other keys or display an alternative message
        print("No summary available. Key findings:")
        for key in solution:
            if isinstance(solution[key], str) and len(solution[key]) < 100:
                print(f"- {key}: {solution[key]}")
            elif isinstance(solution[key], str):
                print(f"- {key}: {solution[key][:100]}...")
            elif isinstance(solution[key], dict) and 'conclusion' in solution[key]:
                print(f"- {key} conclusion: {solution[key]['conclusion']}")
            elif isinstance(solution[key], list) and len(solution[key]) > 0:
                print(f"- {key}: {len(solution[key])} items")
    
    print("\nFor detailed solution, check:", args.output)

if __name__ == "__main__":
    main()