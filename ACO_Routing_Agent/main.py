from llm.llm_interface import LLMInterface

def main():
    print("Enter your query (for example, 'give me the shortest path from Boston Logan Airport to Northeastern University'):")
    user_query = input("> ")
    llm_interface = LLMInterface()
    response = llm_interface.query(user_query)
    print("\nResponse:")
    print(response)

if __name__ == "__main__":
    main()
