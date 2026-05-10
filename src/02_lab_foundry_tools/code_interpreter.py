from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import OpenAI

token_provider = get_bearer_token_provider(
    DefaultAzureCredential(), "https://ai.azure.com/.default"
)

client = OpenAI(  
  base_url ="<BASE_URL>"  #Example "https://ai-103-exam-resource.openai.azure.com/openai/v1",  
  api_key=token_provider,
)

# Get response using the code_interpreter tool
response = client.responses.create(
    model="gpt-5.1",
    instructions="You are an AI assistant that provides information."
                "Use the python tool to run code for math problems.",
    input="What is the square root of 16?",
    tools=[{"type": "code_interpreter", "container": {"type": "auto"}}]
)
print(response.output_text)