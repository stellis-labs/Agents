import streamlit as st
from google import genai
import os
import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent  # Correct for your structure
sys.path.append(str(root_dir))

from dotenv import load_dotenv
from Agents.swarm import SwarmIntelligenceAgent

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key = GEMINI_API_KEY)

# Set a default model
if "genai_model" not in st.session_state:
    st.session_state["genai_model"] = "gemini-2.0-flash"

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# problem_description = "Optimize better way to travel from Boston to Newyork City"
# constraints = "Must be cost-effective and relatively quick."

# Accept user input
if prompt := st.chat_input("Start Typing...."):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    st.chat_message("user").write(prompt)

    agent = SwarmIntelligenceAgent(prompt, "Must be cost-effective and relatively quick.")
    final_solution = agent.solve()

    st.chat_message("assistant").write(final_solution)

    st.session_state.messages.append({"role": "assistant", "content": final_solution})