# utils.py
import json
from src.logger import log

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
    
    # Iterate through the chunks and accumulate the response
    for chunk in response.iter_lines():
        if chunk:
            try:
                chunk_data = validate_json(chunk)  # Validate each chunk
                chunk_content = chunk_data.get("response", "")
                full_response += chunk_content  # Accumulate content in full_response
            except (json.JSONDecodeError, KeyError):
                log("Retrying due to invalid JSON response...", style="bold yellow")
                continue  # Skip invalid chunks and continue processing
    return full_response



