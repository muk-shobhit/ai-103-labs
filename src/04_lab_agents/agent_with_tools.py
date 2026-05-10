import warnings
warnings.simplefilter("ignore")

# Add references
from random import randint
from typing import Annotated
from agent_framework import tool, Agent
from agent_framework.foundry import FoundryChatClient
from agent_framework.observability import disable_instrumentation
from azure.identity import AzureCliCredential
from pydantic import Field
import asyncio

PROJECT_ENDPOINT = "<YOUR_PROJECT_ENDPOINT>"  #Example "https://ai-103-exam.services.ai.azure.com/api/projects/ai-103-exam-project"
MODEL_DEPLOYMENT_NAME = "gpt-4.1"

disable_instrumentation()

credential = AzureCliCredential()                                                                                     

@tool
def get_weather(
    location: Annotated[str, Field(description="The location to get the weather for.")],
) -> str:
    """Get the weather for a given location."""
    conditions = ["sunny", "cloudy", "rainy", "stormy"]
    return f"The weather in {location} is {conditions[randint(0, 3)]} with a high of {randint(10, 30)}°C."


client = FoundryChatClient(                                                                                        
    project_endpoint=PROJECT_ENDPOINT,
    model=MODEL_DEPLOYMENT_NAME,
    credential=credential,
)

agent = Agent(
    client=client,
    name="WeatherAgent",
    instructions="You are a helpful weather agent. Use the get_weather tool to answer questions.",
    tools=[get_weather],
)

async def _main():
    return await agent.run("What is the weather in London?")

result = asyncio.run(_main())
print(f"Agent: {result}")
