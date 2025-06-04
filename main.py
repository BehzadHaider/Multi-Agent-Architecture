import os
import argparse
from agentpro import ReactAgent
from agentpro.tools import QuickInternetTool, CalculateTool, UserInputTool, AresInternetTool, YFinanceTool, TraversaalProRAGTool, SlideGenerationTool,TextSummarizerTool, GrammarCorrectionTool, SentimentAnalysisTool, RestaurantHotelFinderTool
from agentpro import create_model
import litellm
from dotenv import load_dotenv
import os
load_dotenv()
from openai import OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
def main():
    try:
        # Set up argument parser
        parser = argparse.ArgumentParser(description='Run AgentPro with a query')
        parser.add_argument('input_text', type=str, help='The query to process')
        parser.add_argument('--system_prompt', type=str, help='Custom system prompt for the agent', default=None)
        args = parser.parse_args()
        openai_key = os.getenv("OPENAI_API_KEY")
        load_dotenv()
        #litellm._turn_on_debug()
        # Create a model with LiteLLM
        llm_model = create_model(

            provider="litellm",
            model_name="gpt-4o",
            api_key=openai_key,
            litellm_provider="openai",
            temperature=0.7,
            max_tokens=2048
        )

        
        openai_key = os.getenv("OPENAI_API_KEY")

        # Instantiate your tools
        tools = [
            QuickInternetTool(),
            CalculateTool(),
            UserInputTool(),
            YFinanceTool(),
            SlideGenerationTool(),
            AresInternetTool(api_key=os.getenv("ARES_API_KEY", None)),
            TextSummarizerTool(),
            GrammarCorrectionTool(),
            SentimentAnalysisTool(),
            RestaurantHotelFinderTool(),
            # TraversaalProRAGTool(api_key=os.getenv("TRAVERSAAL_PRO_API_KEY", None), document_names="employee_safety_manual"),
        ]
        myagent = ReactAgent(model=llm_model, tools=tools, custom_system_prompt=args.system_prompt, max_iterations=10)
        
        query = args.input_text
        response = myagent.run(query)

        print("=" * 50 + " FINAL Thought Process:")
        for step in response.thought_process:
            if step.pause_reflection:
                print(f"✅ Pause: {step.pause_reflection}")
            if step.thought:
                print(f"✅ Thought: {step.thought}")
            if step.action:
                print(f"✅ Action: {step.action.model_dump_json()}")
            if step.observation:
                print(f"✅ Observation: {step.observation.result}")
        
        print(f"\n✅ Final Answer: {response.final_answer}")

        
    except Exception as e:
        print(f"Error running agent: {e}")

if __name__ == "__main__":
    main()
