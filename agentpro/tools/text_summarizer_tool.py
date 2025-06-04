#from .base_tool import Tool
from .base_tool import Tool
import os
import json
from typing import Any
from pydantic import BaseModel
from abc import ABC, abstractmethod
from dotenv import load_dotenv
load_dotenv()
# Import OpenAI (or LiteLLM) for summarization
from openai import  OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class TextSummarizerTool(Tool):
    name: str = "Text Summarizer"
    description: str ="Summarizes a given block of text into a concise, coherent summary of 3 lines."
    action_type: str = "summarize_text"
    input_format: str = """
Either a raw text string or a JSON object with the following structure:
{
  "text": "string (the full text you want summarized)"
}
"""    

    def run(self, input_text: Any) -> str:
        """
        Summarize the provided text using OpenAI’s ChatCompletion endpoint.
        If `input_text` is JSON, it should contain a "text" field. Otherwise,
        it treats `input_text` as the raw text to summarize.
        """
        print(f"🧪 [Debug] Input received: {repr(input_text)}")
        try:
            # 1) Parse input: if it’s JSON, extract the "text" field; otherwise use it directly
            if isinstance(input_text, str):
                # Try parsing as JSON; if that fails, assume raw text
                try:
                    parsed = json.loads(input_text)
                    text_to_summarize = parsed.get("text", "")
                    if not isinstance(text_to_summarize, str) or text_to_summarize.strip() == "":
                        return "Error: JSON must include a non-empty \"text\" field."
                except json.JSONDecodeError:
                    # Not valid JSON → treat input_text itself as raw text
                    text_to_summarize = input_text
            else:
                return "Error: Input must be either a JSON string or plain text."

            # 2) Ensure we have something to summarize
            if not text_to_summarize.strip():
                return "Error: No text provided to summarize."

            # 3) Load the API key from environment
            openai_api_key = os.getenv("OPENAI_API_KEY")
            if not openai_api_key:
                return "Error: OPENAI_API_KEY environment variable is not set."

            #openai.api_key = openai_api_key

            # 4) Build a prompt that asks the model to summarize concisely
            prompt = (
                "Please provide a concise summary of the following text in 3 lines:\n\n"
                f"{text_to_summarize}\n\n"
                "Summarize it in one coherent paragraph."
            )


            response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
        {"role": "system", "content": "You are a helpful assistant that specializes in creating concise summaries."},
        {"role": "user", "content": prompt}
                ],
    temperature=0.3,
    max_tokens=200
)

            # 6) Extract and return the summary text
            summary = response.choices[0].message.content.strip()
            return summary

        except Exception as e:
            return f"Error during summarization: {str(e)}"
