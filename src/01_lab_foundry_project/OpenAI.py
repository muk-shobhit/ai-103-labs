from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://ai.azure.com/.default"
)

openai_client = OpenAI(  
  base_url =  "<BASE_URL>"  #Example "https://ai-103-exam-resource.openai.azure.com/openai/v1",  
  api_key=token_provider,
)

response = openai_client.responses.create(
        model="gpt-5.1",
        input="What is the size of France in square miles?",
    )
print(f"Response output: {response.output_text}")