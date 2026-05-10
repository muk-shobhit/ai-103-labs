from azure.identity import DefaultAzureCredential
from azure.ai.textanalytics import TextAnalyticsClient
from dotenv import load_dotenv
import os

load_dotenv()

FOUNDRY_ENDPOINT = os.environ.get("FOUNDRY_RESOURCE_OPENAI_ENDPOINT")

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://ai.azure.com/.default"
)

openai_client = OpenAI(base_url = FOUNDRY_ENDPOINT, api_key=token_provider)

user_prompt = "How do you say 'How are you?' in French?"

response = openai_client.responses.create(
    input=[{"role": "user", "content": user_prompt}],
    extra_body={
        "agent_reference": {
            "name": "Text-Analysis-Agent",
            "type": "agent_reference"
        }
    },
)

print(response.output_text)