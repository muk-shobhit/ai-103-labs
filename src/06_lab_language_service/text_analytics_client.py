from azure.identity import DefaultAzureCredential
from azure.ai.textanalytics import TextAnalyticsClient
from dotenv import load_dotenv
import os

load_dotenv()

credential = DefaultAzureCredential()
FOUNDRY_ENDPOINT = os.environ.get("FOUNDRY_RESOURCE_ENDPOINT")

client = TextAnalyticsClient(endpoint=FOUNDRY_ENDPOINT, credential=credential)

documents = ["Hello World!", "Bonjour le monde!"]

# Detect language
# response = client.detect_language(documents=documents)

# for doc in response:
#     print(f"Document: {doc.id}")
#     print(f"\tPrimary Language: {doc.primary_language.name}")
#     print(f"\tISO6391 Name: {doc.primary_language.iso6391_name}")
#     print(f"\tConfidence Score: {doc.primary_language.confidence_score}")


##############################################################################

print("\n Detecting language with a document that has a mix of languages...\n")

documents = ["Je connais un développeur d'IA génial. He has a certain je ne sais quoi!"]

# Detect language
response = client.detect_language(documents=documents)

for doc in response:
    print(f"Document: {doc.id}")
    print(f"\tPrimary Language: {doc.primary_language.name}")
    print(f"\tISO6391 Name: {doc.primary_language.iso6391_name}")
    print(f"\tConfidence Score: {doc.primary_language.confidence_score}")

