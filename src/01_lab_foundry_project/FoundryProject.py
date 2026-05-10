from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

project_endpoint = "<YOUR_PROJECT_ENDPOINT>"

#Example
# project_endpoint = "https://ai-103-exam-resource.services.ai.azure.com/api/projects/ai-103-exam-project"

project_client = AIProjectClient(
    credential=DefaultAzureCredential(),
    endpoint=project_endpoint
)

with project_client.get_openai_client() as openai_client:
    response = openai_client.responses.create(
        model="gpt-5.1",
        input="What is the size of France in square miles?",
    )
    print(f"Response output: {response.output_text}")