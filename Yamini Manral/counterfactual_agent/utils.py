# utils.py
import json
from logger import log

def validate_json(chunk):
    """Validate if the chunk is a valid JSON object."""
    try:
        chunk_data = json.loads(chunk.decode("utf-8"))
        if "response" not in chunk_data:
            raise KeyError("Missing 'response' key in JSON.")
        return chunk_data
    except (json.JSONDecodeError, KeyError) as e:
        log(f"Invalid JSON response: {e}", style="bold yellow")
        raise

def stream_response(response):
    """Stream the response from the LLM API."""
    full_response = ""
    for chunk in response.iter_lines():
        if chunk:
            try:
                chunk_data = validate_json(chunk)
                chunk_content = chunk_data.get("response", "")
                full_response += chunk_content
            except (json.JSONDecodeError, KeyError):
                log("Retrying due to invalid JSON response...", style="bold yellow")
                raise
    return full_response
