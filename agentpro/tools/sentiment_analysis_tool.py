from .base_tool import Tool
import os
import json
from typing import Any
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class SentimentAnalysisTool(Tool):
    name: str = "Sentiment Analyzer"
    description: str = "Analyzes the sentiment of the given text and returns Positive, Negative, or Neutral."
    action_type: str = "analyze_sentiment"
    input_format: str = """
A raw string or a JSON object:
{
  "text": "string (text to analyze sentiment)"
}
"""

    def run(self, input_text: Any) -> str:
        try:
            if isinstance(input_text, dict):
                text = input_text.get("text", "")
            elif isinstance(input_text, str):
                try:
                    parsed = json.loads(input_text)
                    text = parsed.get("text", input_text)
                except json.JSONDecodeError:
                    text = input_text
            else:
                return "Error: Invalid input format."

            if not text.strip():
                return "Error: No text provided."

            prompt = (
                f"Analyze the sentiment of this text and respond only with Positive, Negative, or Neutral:\n\n{text}"
            )

            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a sentiment analysis expert. Respond with only one word: Positive, Negative, or Neutral."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.0,
                max_tokens=10
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            return f"Error during sentiment analysis: {str(e)}"
