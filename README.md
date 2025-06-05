# AgentPro

AgentPro is a lightweight ReAct-style agentic framework built in Python, designed for structured reasoning step-by-step using available tools, while maintaining a complete history of Thought → Action → Observation → PAUSE → Final Answer steps.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/License-Apache%202.0-blue" alt="License: Apache 2.0">
</p>

## 📚 Features

- 🔥 ReAct (Reasoning + Acting) agent pattern
- 🛠️ Modular tool system (easy to add your own tools)
- 📜 Clean Thought/Action/Observation/PAUSE parsing
- 📦 Local package structure for easy extension
- 🧠 Powered by any LLM! (Anthropic, Open AI or any other Open source LLMs)

## Quick Start

### Installation

Install agentpro repository using pip:

```bash
pip install git+https://github.com/traversaal-ai/AgentPro.git -q
```
<!--
### Configuration

Create a `.env` file in the root directory with your API keys:

```
OPENAI_API_KEY=your_openai_api_key
TRAVERSAAL_ARES_API_KEY=your_traversaal_ares_api_key
```
Ares internet tool: Searches the internet for real-time information using the Traversaal Ares API. To get `TRAVERSAAL_ARES_API_KEY`. Follow these steps:

1. Go to the [Traversaal API platform](https://api.traversaal.ai/)
2. Log in or create an account
3. Click **"Create new secret key"**
4. Copy the generated key and paste in `.env` file :

### Running the Agent

From the command line:

```bash
python main.py
```

This starts an interactive session with the agent where you can enter queries. -->

### Basic Usage
```python
import os
from agentpro import ReactAgent
from agentpro.tools import AresInternetTool
from agentpro import create_model

# Create a model with OpenAI
model = create_model(provider="openai", model_name="gpt-4o", api_key=os.getenv("OPENAI_API_KEY", None))

# Initialize tools
tools = [AresInternetTool(os.getenv("ARES_API_KEY", None))]

# Initialize agent
agent = ReactAgent(model=model, tools=tools)

# Run a query
query = "What is the height of the Eiffel Tower?"
response = agent.run(query)

print(f"\nFinal Answer: {response.final_answer}")
```
For Ares api key, follow these steps:

1. Go to the [Traversaal API platform](https://api.traversaal.ai/)
2. Log in or create an account
3. Generate your Ares API key from the dashboard.

<!--
You can also use the [Quick Start](https://github.com/traversaal-ai/AgentPro/blob/main/cookbook/quick_start.ipynb) Jupyter Notebook to run AgentPro directly in Colab.
-->
