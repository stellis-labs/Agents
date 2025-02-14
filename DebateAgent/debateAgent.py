import json
import os
import requests
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")


class DebateAgent:
    def __init__(self, data_path):
        self.data_path = data_path
        self.data = self.load_data()

    def load_data(self):
        
        try:
            with open(self.data_path, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_data(self):
        with open(self.data_path, "w") as file:
            json.dump(self.data, file, indent=4)

    def call_llm(self, prompt, max_tokens=150):
        try:
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
            data = {
                "model": "mixtral-8x7b-32768",
                "messages": [{"role": "system", "content": "Summarize this in 500 characters or less."}, {"role": "user", "content": prompt}],
                "temperature": 0.7,
                "max_tokens": max_tokens
            }
            response = requests.post(url, json=data, headers=headers).json()
            return response.get("choices", [{}])[0].get("message", {}).get("content", "No response.")
        except Exception:
            return "Error in LLM response."

    def get_existing_debate(self, question):
        for debate in self.data:
            if debate["question"].lower() == question.lower():
                return debate
        return None

    def fetch_missing_data(self, perspectives, existing_data):
        logic = existing_data.get("logic", [])
        strengths_weaknesses = existing_data.get("strengths_weaknesses", [])

        # Fetch missing logical consistency analysis
        if not logic:
            print("\n🔍 Fetching logical consistency analysis from LLM...")
            logic = [
                {"label": p["label"], "logic": self.call_llm(f"Analyze logical consistency and weaknesses of: {p['argument']}")}
                for p in perspectives
            ]

        # Fetch missing strengths and weaknesses
        if not strengths_weaknesses:
            print("\n🔍 Fetching strengths and weaknesses from LLM...")
            strengths_weaknesses = [
                {
                    "label": p["label"],
                    "strength": self.call_llm(f"What is the strongest point of this argument: {p['argument']}"),
                    "weakness": self.call_llm(f"What is the biggest flaw in this argument: {p['argument']}")
                }
                for p in perspectives
            ]

        return logic, strengths_weaknesses

    def debate(self, problem):
        stored_debate = self.get_existing_debate(problem)

        if stored_debate:
            print("\n📚 Retrieving existing debate from database...\n")
            perspectives = [
                {"label": f"Perspective {i+1}", "argument": arg["argument"], "evidence": arg.get("evidence", ["No evidence available."])}
                for i, arg in enumerate(stored_debate["arguments"])
            ]
            conclusion = stored_debate.get("conclusion", "No conclusion available.")
            logic, strengths_weaknesses = self.fetch_missing_data(perspectives, stored_debate)
        else:
            print("\n🤖 Generating debate arguments using AI...\n")
            perspectives = self.generate_perspectives(problem)
            evidence = self.evaluate_evidence(perspectives)
            logic = self.check_logical_consistency(perspectives)
            strengths_weaknesses = self.identify_strengths_weaknesses(perspectives)
            conclusion = self.synthesize_conclusion(perspectives, problem)

            self.data.append({
                "question": problem,
                "arguments": [{"argument": p["argument"], "evidence": e["evidence"]} for p, e in zip(perspectives, evidence)],
                "logic": logic,
                "strengths_weaknesses": strengths_weaknesses,
                "conclusion": conclusion
            })
            self.save_data()

        print("\n" + "=" * 80)
        print(f" **Debate Analysis**")
        print("=" * 80)
        print(f" **Issue:** {problem}\n")

        print(" **Step 1: Generate Opposing Perspectives**")
        for p in perspectives:
            print(f"   • **{p['label']}** → {p['argument']}")

        print("\n **Step 2: Evaluate Evidence & Precedents**")
        for p in perspectives:
            print(f"   • **{p['label']}** Evidence → {p.get('evidence', 'No evidence available.')}")

        print("\n **Step 3: Check Logical Consistency**")
        for l in logic:
            print(f"   • **{l['label']}** → {l.get('logic', 'No logic analysis available.')}")

        print("\n **Step 4: Identify Strengths & Weaknesses**")
        for s in strengths_weaknesses:
            print(f"   • **{s['label']}** → **Strength:** {s.get('strength', 'No data available')} | **Weakness:** {s.get('weakness', 'No data available')}")

        print("\n **Step 5: Synthesize Conclusion**")
        print(f"   → {conclusion}")
        print("=" * 80)


# User Interaction Loop
if __name__ == "__main__":
    agent = DebateAgent("procon_debates.json")

    while True:
        problem = input("\n Enter a debate question (or type 'exit' to quit): ").strip()
        if problem.lower() == "exit":
            print("\n Exiting Debate Agent. Have a great day!")
            break
        if not problem:
            print(" Please enter a valid question.")
            continue
        agent.debate(problem)
