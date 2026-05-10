from azure.identity import DefaultAzureCredential
from azure.ai.projects.models import MCPTool
from azure.ai.projects import AIProjectClient
from dotenv import load_dotenv
import os

load_dotenv()

FOUNDRY_ENDPOINT = os.environ.get("FOUNDRY_RESOURCE_ENDPOINT")
FOUNDRY_RESOURCE_NAME = os.environ.get("FOUNDRY_RESOURCE_NAME")
FOUNDRY_MODEL = os.environ.get("FOUNDRY_MODEL")

project_client = AIProjectClient(
    endpoint=FOUNDRY_ENDPOINT,
    credential=DefaultAzureCredential(),
)

openai_client = project_client.get_openai_client()

prompt = input("User prompt: ")

response = openai_client.responses.create(
    input=[{"role": "user", "content": prompt}],
    extra_body={"agent_reference": {"name": agent_name, "type": "agent_reference"}},
)

print(f"{agent_name}: {response.output_text}")