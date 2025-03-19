import re
import json
import json5

def clean_response(text: str) -> str:
    # Remove <think> blocks.
    text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    # Remove markdown code fences.
    text = re.sub(r'```(?:json)?', '', text)
    # Remove markdown markers (e.g., ** or *).
    text = re.sub(r'\*+', '', text)
    # Remove any leading headings like "Solution:" or "Response:".
    text = re.sub(r'^(Solution:|Response:)\s*', '', text, flags=re.IGNORECASE)
    text = text.strip()
    # Check if the response is in numbered list format.
    lines = text.splitlines()
    numbered_lines = []
    for line in lines:
        match = re.match(r'^\s*\d+\.\s*(.*)', line)
        if match:
            numbered_lines.append(match.group(1).strip())
    if numbered_lines:
        return json.dumps(numbered_lines)
    # Otherwise, if there is a JSON object or array present, extract from the first occurrence.
    idx_obj = text.find("{")
    idx_arr = text.find("[")
    if idx_obj == -1 and idx_arr == -1:
        return text.strip()
    if idx_obj == -1:
        idx = idx_arr
    elif idx_arr == -1:
        idx = idx_obj
    else:
        idx = min(idx_obj, idx_arr)
    return text[idx:].strip()
