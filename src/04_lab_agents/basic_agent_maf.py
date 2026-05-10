import warnings
warnings.simplefilter("ignore")

# Add references
from agent_framework import Agent
from agent_framework.foundry import FoundryChatClient
from agent_framework.observability import disable_instrumentation
from azure.identity import AzureCliCredential
import asyncio

PROJECT_ENDPOINT = "<YOUR_PROJECT_ENDPOINT>"  #Example "https://ai-103-exam.services.ai.azure.com/api/projects/ai-103-exam-project"
MODEL_DEPLOYMENT_NAME = "gpt-4.1"

disable_instrumentation()

credential = AzureCliCredential()                                                                                     

client = FoundryChatClient(                                                                                        
    project_endpoint=PROJECT_ENDPOINT,
    model=MODEL_DEPLOYMENT_NAME,
    credential=credential,
)

instructions="""
    You are a helpful General Knowledge assistant.
    Always respond professionally, clearly, and concisely.
    """
        
agent = Agent(                                                                                               
    client=client,
    name="HelloAgent",
    instructions=instructions,
)

result = asyncio.run(agent.run("\nWhat is the largest city in India?"))
print(f"Agent: {result}")
