import google.generativeai as genai
import logging
import time
import random
from typing import List, Tuple

logger = logging.getLogger(__name__)

class GeminiClient:
    def __init__(self, keys: List[str], model_name: str = "gemini-2.0-flash-exp"):
        self.keys = keys
        self.model_name = model_name
        self.current_key_index = 0
        self._configure_client()

    def _configure_client(self):
        if not self.keys:
            raise ValueError("No Gemini API keys provided.")
        
        current_key = self.keys[self.current_key_index]
        genai.configure(api_key=current_key)
        logger.info(f"Switched to Gemini API Key index: {self.current_key_index}")

    def _rotate_key(self):
        self.current_key_index = (self.current_key_index + 1) % len(self.keys)
        self._configure_client()

    def analyze_market(self, title: str, description: str) -> Tuple[str, str]:
        """
        Analyzes a market and returns a recommendation (YES/NO) and reasoning.
        """
        prompt = f"""
        You are a prediction market expert. Analyze the following market and recommend whether to bet YES or NO based on the likelihood of the event occurring.
        
        Market Title: {title}
        Market Description: {description}
        
        Provide your response in the following format:
        DECISION: [YES/NO]
        REASONING: [Brief explanation of your decision, max 2 sentences]
        """

        retries = len(self.keys)
        for _ in range(retries):
            try:
                model = genai.GenerativeModel(self.model_name)
                response = model.generate_content(prompt)
                
                text = response.text.strip()
                lines = text.split('\n')
                decision = "UNKNOWN"
                reasoning = "Could not parse response."
                
                for line in lines:
                    if line.startswith("DECISION:"):
                        decision = line.replace("DECISION:", "").strip().upper()
                    elif line.startswith("REASONING:"):
                        reasoning = line.replace("REASONING:", "").strip()
                
                return decision, reasoning

            except Exception as e:
                logger.error(f"Gemini API error with key index {self.current_key_index}: {e}")
                self._rotate_key()
                time.sleep(1) # Brief pause before retry
        
        return "ERROR", "Failed to get recommendation after trying all keys."
