import json
import logging
import re
import requests
from typing import Dict, Any, Optional

class OllamaClient:
    """Client for interacting with the Ollama API."""

    def __init__(self, model: str = "llama3.1:latest", host: str = "localhost", port: int = 11434):
        """
        Initialize the Ollama client.
        
        Args:
            model: The model to use for generation (default: "llama3.1:latest")
            host: Ollama server host (default: "localhost")
            port: Ollama server port (default: 11434)
        """
        self.model = model
        self.base_url = f"http://{host}:{port}"
        self.logger = logging.getLogger("FRA.OllamaClient")
        logging.basicConfig(level=logging.INFO)
        self.logger.info(f"Initialized Ollama client with model {model}")

    def generate(self, prompt: str, system_prompt: Optional[str] = None,
                 max_tokens: int = 2048, temperature: float = 0.7) -> Dict[str, Any]:
        """
        Generate a response using the Ollama API.
        
        Args:
            prompt: The user prompt
            system_prompt: Optional system prompt to guide the model
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature (0.0 to 1.0)
        
        Returns:
            Dict containing the response
        """
        url = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": temperature,
        }
        if system_prompt:
            payload["system"] = system_prompt
        
        try:
            response = requests.post(url, json=payload, stream=True)
            response.raise_for_status()
            
            # Concatenate the streaming response
            full_response = ""
            for line in response.iter_lines():
                if line:
                    json_chunk = json.loads(line)
                    full_response += json_chunk.get("response", "")
            
            # Log the raw API response for debugging
            self.logger.debug(f"Raw API Response:\n{full_response}")
            
            return self._extract_json(full_response)
        except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
            self.logger.error(f"Error calling Ollama API: {e}")
            return {"error": "API request failed", "details": str(e)}

    def generate_structured(self, prompt: str, instruction: str,
                            output_format: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a structured response with specific format instructions.
        
        Args:
            prompt: The user prompt
            instruction: Specific instruction for this generation
            output_format: Dictionary describing the expected output format
        
        Returns:
            Dict containing the structured response
        """
        system_prompt = (
            "You are a component of a Fractal Reasoning Agent designed to solve complex problems. "
            "Always respond with valid JSON according to the requested output format. "
            "Think step-by-step and be thorough in your analysis."
        )
        formatted_prompt = f"""
        {instruction}
        
        Input:
        {prompt}
        
        Expected output format:
        {json.dumps(output_format, indent=2)}
        
        Provide your response as valid JSON following this format exactly.
        """
        response = self.generate(formatted_prompt, system_prompt, temperature=0.2)
        return response

    def _extract_json(self, text: str) -> Dict[str, Any]:
        """
        Extract JSON data from a given text response.
        
        Args:
            text: The raw API response text
        
        Returns:
            A dictionary containing the extracted JSON data
        """
        try:
            # Attempt to parse the entire response as JSON
            return json.loads(text)
        except json.JSONDecodeError:
            self.logger.debug("Direct JSON parsing failed. Attempting extraction...")
            
            # First, check if this is a streamed response with multiple JSON objects
            try:
                # For Ollama's streaming format, we need to collect the actual response
                # from multiple JSON lines and concatenate them
                lines = text.strip().split('\n')
                collected_response = ""
                final_context = None
                final_duration = None
                
                for line in lines:
                    try:
                        obj = json.loads(line)
                        if 'response' in obj:
                            collected_response += obj['response']
                        if obj.get('done', False) and 'context' in obj:
                            final_context = obj['context']
                            final_duration = obj.get('total_duration')
                    except json.JSONDecodeError:
                        continue
                
                # If we collected a response, try to parse it as JSON
                if collected_response:
                    try:
                        # Clean the collected response - it might be a JSON string
                        cleaned_response = collected_response.strip()
                        
                        # Try to parse the collected content as JSON
                        parsed_content = json.loads(cleaned_response)
                        
                        # Add metadata from the final response if available
                        if final_context:
                            parsed_content['_metadata'] = {
                                'context': final_context,
                                'total_duration': final_duration
                            }
                        
                        return parsed_content
                    except json.JSONDecodeError:
                        # The collected response is not valid JSON, return the raw text
                        return {"content": cleaned_response, "is_structured": False}
            except Exception as e:
                self.logger.debug(f"Streaming response handling failed: {e}")
            
            # If streaming approach failed, try traditional JSON extraction
            try:
                # Remove any leading/trailing non-JSON content
                text = text.strip()
                if text.startswith("```json"):
                    text = text[7:].strip()  # Remove ```json
                if text.endswith("```"):
                    text = text[:-3].strip()  # Remove ```

                # Attempt to parse the cleaned text as JSON
                return json.loads(text)
            except json.JSONDecodeError:
                self.logger.debug("Cleaned text parsing failed. Attempting to find JSON block...")

                # Try to find a JSON object in the response
                json_pattern = re.compile(r'\{(?:[^{}]|(?:\{(?:[^{}]|(?:\{(?:[^{}])*\}))*\}))*\}')
                matches = json_pattern.findall(text)
                if matches:
                    for potential_json in matches:
                        try:
                            result = json.loads(potential_json)
                            return result
                        except json.JSONDecodeError:
                            continue

        # If all else fails, return an error with the raw response
        self.logger.error("Could not extract valid JSON from response")
        truncated_text = text[:500] + "..." if len(text) > 500 else text
        self.logger.debug(f"Raw response (truncated):\n{truncated_text}")
        return {"error": "No valid JSON found", "raw_response": text[:1000]}