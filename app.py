# app.py
import os
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# AgentPro imports
import litellm
from openai import OpenAI

from agentpro import ReactAgent, create_model
from agentpro.tools import (
    QuickInternetTool,
    CalculateTool,
    UserInputTool,
    AresInternetTool,
    YFinanceTool,
    TraversaalProRAGTool,
    SlideGenerationTool,
    TextSummarizerTool,
    SentimentAnalysisTool,
    GrammarCorrectionTool,
    RestaurantHotelFinderTool,
    EventAggregatorTool,
)


st.set_page_config(
    page_title="BLLMA - Demo",
    layout="wide",
)

st.title("🔍 Building Real functioning AI Agent leveraging a Multi-Agent Architecture By Behzad Haider(2430-6050)")
st.markdown(
    """
Enter a query below and click **Run Agent**.  
You can also specify a custom system prompt (optional).  
The thought process and final answer will appear below.
"""
)

# Sidebar for optional configuration
with st.sidebar:
    st.header("⚙️ Configuration")

    # Custom system prompt (optional)
    custom_prompt = st.text_area(
        "Custom System Prompt (optional)",
        value="",
        help="If provided, this prompt will override the default system prompt."
    )

    # LLM settings (temperature, max_tokens, etc.)
    st.subheader("LLM Settings")
    temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        value=0.7,
        step=0.1,
        help="Controls randomness of the model."
    )
    max_tokens = st.number_input(
        "Max Tokens",
        min_value=256,
        max_value=4096,
        value=2048,
        step=256,
        help="Maximum tokens for the LLM response."
    )

st.markdown("---")

# User input for the query
query = st.text_input(
    "Enter your query:",
    placeholder="E.g. Provide me list of 5 best restaurants in Islamabad? Or summarize the following text...",
)

run_button = st.button("🕵️‍♂️ Run Agent")

# Only execute when the button is clicked
if run_button:
    if not query.strip():
        st.error("Please enter a valid query before running the agent.")
    else:
        # Show a spinner while running the agent
        with st.spinner("Running AgentPro..."):
            try:
                # 1. Prepare the LLM model
                openai_key = os.getenv("OPENAI_API_KEY")
                if not openai_key:
                    st.error("Environment variable OPENAI_API_KEY is missing.")
                    st.stop()

                llm_model = create_model(
                    provider="litellm",
                    model_name="gpt-4o",
                    api_key=openai_key,
                    litellm_provider="openai",
                    temperature=temperature,
                    max_tokens=max_tokens,
                )

                # 2. Instantiate tools
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
                    EventAggregatorTool(),
                    # If you want to enable RAG, uncomment the next line and set TRAVERSAAL_PRO_API_KEY in your .env
                    # TraversaalProRAGTool(api_key=os.getenv("TRAVERSAAL_PRO_API_KEY", None), document_names="employee_safety_manual"),
                ]

                # 3. Instantiate the ReactAgent
                myagent = ReactAgent(
                    model=llm_model,
                    tools=tools,
                    custom_system_prompt=custom_prompt if custom_prompt.strip() else None,
                    max_iterations=10,
                )

                # 4. Run the agent on the user’s query
                response = myagent.run(query)

                # 5. Display the thought process
                st.subheader("🧠 Thought Process")
                for idx, step in enumerate(response.thought_process, start=1):
                    st.markdown(f"**Step {idx}:**")
                    if step.pause_reflection:
                        st.markdown(f"> **Pause:** {step.pause_reflection}")
                    if step.thought:
                        st.markdown(f"> **Thought:** {step.thought}")
                    if step.action:
                        # Display the action JSON in a code block
                        action_json = step.action.model_dump_json()
                        st.markdown("> **Action:**")
                        st.code(action_json, language="json")
                    if step.observation:
                        st.markdown(f"> **Observation:** {step.observation.result}")
                    st.markdown("---")

                # 6. Display the final answer
                st.subheader("✅ Final Answer")
                st.write(response.final_answer)

            except Exception as e:
                st.error(f"Error running agent: {e}")
