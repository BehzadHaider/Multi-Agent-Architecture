from .base_tool import Tool
import os
import json
from typing import Any
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class RestaurantHotelFinderTool(Tool):
    name: str = "Restaurant & Hotel Finder"
    description: str = "Finds top-rated restaurants and hotels based on location and preferences."
    action_type: str = "find_restaurants_and_hotels"
    input_format: str = """
A JSON object with optional fields:
{
  "location": "City or place name (e.g., New York, Lahore)",
  "type": "restaurant or hotel",
  "preference": "optional string like 'Italian', '5-star', 'budget', 'near beach', etc."
}
"""

    def run(self, input_data: Any) -> str:
        try:
            # Parse input
            if isinstance(input_data, dict):
                location = input_data.get("location", "").strip()
                type_ = input_data.get("type", "").strip().lower()
                preference = input_data.get("preference", "").strip()
            elif isinstance(input_data, str):
                try:
                    parsed = json.loads(input_data)
                    location = parsed.get("location", "").strip()
                    type_ = parsed.get("type", "").strip().lower()
                    preference = parsed.get("preference", "").strip()
                except json.JSONDecodeError:
                    return "Error: Invalid JSON string format."
            else:
                return "Error: Invalid input format."

            if not location or type_ not in ["restaurant", "hotel"]:
                return "Error: Please provide a valid 'location' and 'type' (restaurant or hotel)."

            # Generate prompt
            prompt = f"""You are a travel expert. Suggest the 5 best {type_}s in {location}.
Preference: {preference if preference else "No specific preference."}
Format:
1. Name - Short description - Rating (out of 5)
Only provide the list. Do not include any other text.
"""

            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a travel expert helping users find highly-rated places."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=300
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            return f"Error while finding restaurants/hotels: {str(e)}"
