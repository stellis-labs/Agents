# llm_api.py
import time
import json
import requests
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from config import LLM_API_URL, COST_THRESHOLD, TIME_LIMIT
from logger import log

api_call_count = 0
start_time = time.time()

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10),
    retry=retry_if_exception_type((json.JSONDecodeError, KeyError)),
)
def call_llm(prompt):
    """Call the LLM API with the given prompt."""
    global api_call_count

    if api_call_count >= COST_THRESHOLD:
        raise Exception("Cost threshold exceeded. Stopping further API calls.")
    if time.time() - start_time > TIME_LIMIT:
        raise Exception("Time limit exceeded. Stopping execution.")

    api_call_count += 1

    try:
        response = requests.post(
            LLM_API_URL,
            json={"model": "llama3.1:latest", "prompt": prompt, "stream": True},
            stream=True,
        )
        response.raise_for_status()
        return response
    except Exception as e:
        log(f"Error calling LLM API: {e}", style="bold red")
        raise
