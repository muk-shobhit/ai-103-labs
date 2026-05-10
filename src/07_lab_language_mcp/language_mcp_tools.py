import warnings
warnings.simplefilter("ignore")
from azure.ai.projects.models import MCPTool
from agent_framework.observability import disable_instrumentation
from dotenv import load_dotenv
from azure.identity import AzureCliCredential
from agent_framework.foundry import FoundryChatClient
from agent_framework import tool, Agent
import asyncio
import os
load_dotenv()
disable_instrumentation()

FOUNDRY_ENDPOINT = os.environ.get("FOUNDRY_ENDPOINT")
FOUNDRY_RESOURCE_NAME = os.environ.get("FOUNDRY_RESOURCE_NAME")
FOUNDRY_MODEL = os.environ.get("FOUNDRY_MODEL")
FOUNDRY_PROJECT_KEY = os.environ.get("FOUNDRY_PROJECT_KEY")

mcp_tool = MCPTool(
    server_label="azure-language",
    server_url=f"https://{FOUNDRY_RESOURCE_NAME}.cognitiveservices.azure.com/language/mcp?api-version=2025-11-15-preview",
    require_approval="always",
    headers={
        "Ocp-Apim-Subscription-Key": FOUNDRY_PROJECT_KEY
    }
)

credential = AzureCliCredential()                                                                                     

client = FoundryChatClient(                                                                                        
    project_endpoint=FOUNDRY_ENDPOINT,
    model=FOUNDRY_MODEL,
    credential=credential,
)

user_prompt = "How do you say 'How are you?' in French?"

agent = Agent(                                                                                               
    client=client,
    name="LanguageAgent",
    instructions="You are an AI agent that assists users by helping them analyze text."
                 "Use the Azure Language tool to perform text analysis tasks.",
    tools=[mcp_tool]
)

result = asyncio.run(agent.run(user_prompt))
print(f"Agent: {result}")