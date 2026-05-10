from azure.identity import DefaultAzureCredential
from azure.ai.textanalytics import TextAnalyticsClient
from dotenv import load_dotenv
import os

load_dotenv()

credential = DefaultAzureCredential()
FOUNDRY_ENDPOINT = os.environ.get("FOUNDRY_RESOURCE_ENDPOINT")

client = TextAnalyticsClient(endpoint=FOUNDRY_ENDPOINT, credential=credential)

documents = ["John Smith works at Contoso Ltd. His email is john.smith@contoso.com and his phone number is 555-012-456.",
             "Patient Sarah Johnson, SSN 123-45-6789, was admitted on 03/15/2024."]        

# Redact PII entities
response = client.recognize_pii_entities(documents=documents, language="en")
for doc in response:
    print(f"\nDocument {doc.id} (redacted):")
    print(f" {doc.redacted_text}")         