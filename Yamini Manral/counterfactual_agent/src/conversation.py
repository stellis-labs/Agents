# conversation.py
import time
import sys
from rich.console import Console
# from src.llm_api import call_llm
# from src.utils import stream_response
from src.agent import CounterfactualAgent
from src.logger import log_markdown
# from collections import Counter
import re

console = Console()

class ChatSession:
    """Handles a single conversation session."""

    def __init__(self):
        self.active_question = None  # Stores the leading what-if question
        self.counterfactual_agent = None
        self.scenarios = []  # Stores generated scenarios
        self.results = []  # Stores evaluations

    def start(self):

        """Start the chat session with an initial what-if question."""
        
        print("\nWelcome! Start with a 'what-if' question.\n")

        
        if not self.active_question:
            self.active_question = input("🔍 What-if Question: ")
            if "bye" in self.active_question.lower():
                self.exit_session()

            start_time = time.time()
            # Initialize Counterfactual Agent with the user's question
            self.counterfactual_agent = CounterfactualAgent(self.active_question)

            print("\n🔄 Exploring and analysing counterfactual scenarios... This may take some time...")
            self.counterfactual_agent.explore_counterfactuals()  # Generate and evaluate scenarios

            # self.counterfactual_agent.display_final_recommendation()

            elapsed_time = time.time() - start_time
            print("\n")
            log_markdown(f"Time taken: {elapsed_time:.2f} seconds")
            print("\n") 
            self.exit_session()

            # follow_up = input("\nYou (follow-up): ")

            # if "bye" in follow_up.lower():
            #     self.exit_session()
            #     break

            # if not self.is_related_to_main_question(follow_up):
            #     print("\n❗ This follow-up question is not related to the main question. Please stay on topic.")
            #     continue  # Skip irrelevant follow-up questions
            
            # # Call LLM API for follow-up responses based on the original what-if question
            # response = call_llm(f"Based on '{self.active_question}', follow-up: {follow_up}")
            # follow_up_response = stream_response(response)
            
            # # log_markdown(follow_up_response)
            # console.print(f"🤖 AI: {follow_up_response}")

    # def reset_session(self):
    #     """Reset the session for a new what-if question."""
    #     print("\n🔄 Resetting... Start a new what-if question.\n")
    #     self.active_question = None
    #     self.scenarios = []
    #     self.results = []

    # def is_related_to_main_question(self, follow_up):
    #     """Check if the follow-up question is related to the main question."""
        
    #     # Tokenize and clean both the original question and the follow-up question
    #     original_tokens = set(re.findall(r'\w+', self.active_question.lower()))  # Tokens from original question
    #     follow_up_tokens = set(re.findall(r'\w+', follow_up.lower()))  # Tokens from follow-up question
        
    #     # Count the common words between the original question and follow-up
    #     common_tokens = original_tokens.intersection(follow_up_tokens)
    #     print(common_tokens)
        
    #     # If we have some common keywords, assume it's related
    #     if len(common_tokens) > 5:
    #         return True
    #     return False

    def exit_session(self):
        """Exit the session and clean up."""
        print("\n🔴 Exiting the session...\n")
        self.active_question = None
        self.scenarios = []
        self.results = []
        sys.exit()  # Exit the program immediately
