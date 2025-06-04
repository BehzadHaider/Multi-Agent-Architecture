from .base_tool import Tool
import os
import json
from typing import Any
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class GrammarCorrectionTool(Tool):
    name: str = "Grammar Corrector"
    description: str = "Corrects grammatical errors in the provided English text."
    action_type: str = "correct_grammar"
    input_format: str = """
A raw English sentence or a JSON object:
{
  "text": "string (text with grammar issues)"
}
"""

    def run(self, input_text: Any) -> str:
        try:
            if isinstance(input_text, dict):
                text_to_correct = input_text.get("text", "")
            elif isinstance(input_text, str):
                try:
                    parsed = json.loads(input_text)
                    text_to_correct = parsed.get("text", input_text)
                except json.JSONDecodeError:
                    text_to_correct = input_text
            else:
                return "Error: Invalid input format."

            if not text_to_correct.strip():
                return "Error: No text provided."

            prompt = (
                f"Please correct any grammar and punctuation errors in the following text:\n\n{text_to_correct}"
            )

            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a grammar correction expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=200
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            return f"Error during grammar correction: {str(e)}"
