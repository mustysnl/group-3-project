# This file Talks to an external website (an API) to fetch real holiday data

import os
import requests
from dotenv import load_dotenv

load_dotenv()  # it reads the .env file in this folder and loads its values


class CultureGuideGenerator:
    # Asks the Gemini API to explain a holiday's cultural meaning and suggest a greeting

    def __init__(self, api_key=None):
        # The key is read from an environment variable instead of being typed and input it in the GUI 
       
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        self.endpoint = "https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent"

    def generate(self, holiday, country_code):
        if not self.api_key:
            # no key given, so just show a basic message instead of crashing
            return f"{holiday.name} is celebrated in {country_code} on {holiday.date}. (Set GEMINI_API_KEY for an AI explanation.)"

        prompt = (
            f"In 2-3 short sentences, explain the cultural or historical meaning of "
            f"the holiday '{holiday.name}' in country {country_code}, then suggest a short greeting."
        )
        try:
            resp = requests.post(
                f"{self.endpoint}?key={self.api_key}",
                json={"contents": [{"parts": [{"text": prompt}]}]},
                timeout=20,
            )
            resp.raise_for_status()
            data = resp.json()
            return data["candidates"][0]["content"]["parts"][0]["text"].strip()
        except Exception as e:
            return f"(AI explanation unavailable: {e})"