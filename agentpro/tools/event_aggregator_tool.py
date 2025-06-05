from .base_tool import Tool
import requests
from typing import Any
import json

class EventAggregatorTool(Tool):
    name: str = "Event Aggregator"
    description: str = (
        "Collects upcoming public events from Eventbrite API by city and/or keyword."
    )
    action_type: str = "fetch_events"
    input_format: str = (
        "A JSON with 'city' and optional 'keyword' for filtering events.\n"
        "Example: {\"city\": \"San Francisco\", \"keyword\": \"technology\"}"
    )

    def run(self, input_text: Any) -> str:
        if isinstance(input_text, str):
            try:
                input_text = json.loads(input_text)
            except json.JSONDecodeError:
                return "❌ Error: Expected JSON input like {\"city\": \"San Francisco\"}."

        if not isinstance(input_text, dict) or "city" not in input_text:
            return "❌ Error: Missing 'city' field in input."

        city = input_text["city"].strip()
        keyword = input_text.get("keyword", "").strip()

        # Eventbrite public event search API endpoint
        url = "https://www.eventbriteapi.com/v3/events/search/"

        # NOTE: Eventbrite requires an API token. For demo, we'll use a placeholder.
        # Replace 'YOUR_EVENTBRITE_TOKEN' with your actual token if you have one.
        #token = "2WOAH3HAMSK3V4KKEDRV"  old
        token = "VEKISXA3FNE2GTHPQDRK"  #new
        params = {
        "location.address": "Islamabad",
        "expand": "venue",
        "page": 1
                }
        headers = {
        "Authorization": "Bearer VEKISXA3FNE2GTHPQDRK"
        }

        """headers = {
            "Authorization": f"Bearer {token}"
        }"""

        """params = {
            "location.address": city,
            "q": keyword,
            "sort_by": "date",
            "expand": "venue",
            "page": 1,
        }"""


    

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            data = response.json()
        except requests.RequestException as e:
            return f"❌ Error fetching events: {str(e)}"

        events = data.get("events", [])
        if not events:
            return f"No upcoming events found for city '{city}' with keyword '{keyword}'."

        output_lines = [f"Upcoming Events in {city}:"]
        for event in events[:5]:  # limit to first 5 events for brevity
            name = event.get("name", {}).get("text", "N/A")
            start = event.get("start", {}).get("local", "N/A")
            venue = event.get("venue", {}).get("address", {}).get("localized_address_display", "N/A")
            url = event.get("url", "N/A")
            output_lines.append(f"- {name}\n  When: {start}\n  Where: {venue}\n  More info: {url}")

        return "\n\n".join(output_lines)