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
STORAGE_SAS_URL = o



mcp_tool = MCPTool(
    server_label="azure-speech",
    server_url=f"https://{FOUNDRY_RESOURCE_NAME}.cognitiveservices.azure.com/speech/mcp",
    headers={
        "Ocp-Apim-Subscription-Key": FOUNDRY_PROJECT_KEY,
        "X-Blob-Container-Url": STORAGE_SAS_URL
    }
)

client = FoundryChatClient(                                                                                        
    project_endpoint=FOUNDRY_ENDPOINT,
    model=FOUNDRY_MODEL,
    credential=credential,
)

user_prompt = "Generate 'I am speech service and I can help you with speech analysis.' as speech"

agent = Agent(                                                                                               
    client=client,
    name="SpeechAgent",
    instructions="You are an AI agent that uses the Azure AI Speech tool to transcribe and generate speech.",
    tools=[mcp_tool]
)

result = asyncio.run(agent.run(user_prompt))
print(f"Agent: {result}")