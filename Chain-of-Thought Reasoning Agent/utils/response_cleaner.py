import re

class ResponseCleaner:
    @staticmethod
    def clean_response(response: str) -> list:
        cleaned_response = re.sub(r"<think>.*?</think>", "", response, flags=re.DOTALL)
        lines = [line.strip() for line in cleaned_response.split("\n") if line.strip()]
        return lines
