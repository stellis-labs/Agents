import streamlit as st
from groq import Client
import groq
import os
import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent 
sys.path.append(str(root_dir))

from dotenv import load_dotenv
from Agents.swarm import SwarmIntelligenceAgent

load_dotenv()

# Set a default model
if "groq_model" not in st.session_state:
    st.session_state["groq_model"] = "llama-3.1-8b-instant"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# problem_description = "Optimize better way to travel from Boston to Newyork City"
# problem_description = "How can a small business increase its online sales with a limited budget?"
# constraints = "Must be cost-effective and relatively quick."

# Accept user input
if prompt := st.chat_input("Start Typing...."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    st.chat_message("user").write(prompt)

    problem_description = "How can a small business increase its online sales with a limited budget?"
    agent = SwarmIntelligenceAgent(prompt)
    final_solution = agent.solve()

    # Extracting and structuring output
    sections = final_solution.split("\n\n")

    # Extract recommended solutions
    recommended_solutions = sections[0].replace("Recommended Solutions:\n", "").strip().split("\n")

    # Extract final optimized choice
    final_choice = sections[-1].replace("Final Optimized Choice:\n", "").strip()

    print("\n" + "=" * 80)
    print(f"🌱 **PROBLEM STATEMENT:** {problem_description}")
    print("=" * 80)
    print("\n🔍 **RECOMMENDED SOLUTIONS:**\n")

    # Clean up numbered solutions
    for line in recommended_solutions:
        if line.strip() and not line.startswith("Here are"):
            print(f"   ✅ {line.strip()}")

    print("\n" + "=" * 80)
    print("🏆 **FINAL OPTIMIZED CHOICE:**")
    print("=" * 80)
    print(f"💡 {final_choice}")
    print("=" * 80 + "\n")


    st.chat_message("assistant").write(final_solution)

    st.session_state.messages.append({"role": "assistant", "content": final_solution})