from agent import DistributedReasoningAgent

if __name__ == "__main__":
    user_input = input("Enter a problem statement: ")
    agent = DistributedReasoningAgent()
    sub_tasks = agent.generate_sub_tasks(user_input)
    agent.create_sub_agents(sub_tasks)
    agent.execute()
