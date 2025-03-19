import os
import sys
import logging
from dotenv import load_dotenv
from agents.aco_agent import ACOLLMAgent

def setup_logging(level=logging.INFO):
    logger = logging.getLogger("ACOLLMAgent")
    logger.setLevel(level)
    fh = logging.FileHandler("aco_llm.log", encoding="utf-8")
    fh.setLevel(level)
    ch = logging.StreamHandler()
    ch.setLevel(level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)
    return logger

def main():
    load_dotenv()
    logger = setup_logging()
    
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        logger.error("GROQ_API_KEY not found in environment variables.")
        sys.exit(1)
    
    if len(sys.argv) > 1:
        problem_definition = " ".join(sys.argv[1:])
    else:
        problem_definition = input("Enter the ACO problem definition: ")
    
    constraints = "Solutions must be cost-effective, cover the entire service area, and optimize delivery time."
    
    agent = ACOLLMAgent(api_key=api_key, constraints=constraints, max_solutions=5)
    try:
        logger.info("Initializing agent with problem definition")
        agent.initialize(problem_definition)
        
        logger.info("Starting full ACO optimization process")
        results = agent.optimize()
        
        logger.info("Saving results to file")
        agent.save_results("optimization_results.json")
        print("Optimization complete. Results saved to optimization_results.json")
        print("\n" + results.get("formatted_output", "No formatted output available."))
    except Exception as e:
        logger.error(f"Error during optimization: {str(e)}")

if __name__ == "__main__":
    main()
