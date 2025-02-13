# main.py
import time
from agent import CounterfactualAgent
from logger import log

def main():
    question = "What if we increase the marketing budget by 20% for our new product launch?"
    agent = CounterfactualAgent(question)

    start_time = time.time()
    agent.explore_counterfactuals()
    agent.display_final_recommendation()
    
    elapsed_time = time.time() - start_time
    log(f"Time taken: {elapsed_time:.2f} seconds", style="bold green")

if __name__ == "__main__":
    main()
