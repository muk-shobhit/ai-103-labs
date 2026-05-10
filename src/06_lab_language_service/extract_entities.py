from azure.identity import DefaultAzureCredential
from azure.ai.textanalytics import TextAnalyticsClient
from dotenv import load_dotenv
import os

load_dotenv()

credential = DefaultAzureCredential()
FOUNDRY_ENDPOINT = os.environ.get("FOUNDRY_RESOURCE_ENDPOINT")

client = TextAnalyticsClient(endpoint=FOUNDRY_ENDPOINT, credential=credential)

documents = [ "Apple was founded by Steve Jobs, Steve Wozniak, and Ronald Wayne on April 1, 1976 in Cupertino, California.",
    "Tim Cook became CEO of Apple on August 24, 2011.",]

response = client.recognize_entities(documents=documents)

for doc in response:
    print(f"\nEntities in document {doc.id}:")
    for entity in doc.entities:
        print(f" - {entity.text} ({entity.category})")