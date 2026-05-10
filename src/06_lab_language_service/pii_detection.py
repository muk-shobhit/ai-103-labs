from azure.identity import DefaultAzureCredential
from azure.ai.textanalytics import TextAnalyticsClient
from dotenv import load_dotenv
import os

load_dotenv()

credential = DefaultAzureCredential()
FOUNDRY_ENDPOINT = os.environ.get("FOUNDRY_RESOURCE_ENDPOINT")

client = TextAnalyticsClient(endpoint=FOUNDRY_ENDPOINT, credential=credential)

# Example text to analyze
documents = ["John Smith works at Contoso Ltd. His email is john.smith@contoso.com and his phone number is 555-012-456.",
             "Patient Sarah Johnson, SSN 123-45-6789, was admitted on 03/15/2024."]

ORANGE = "\033[93m"  # Bright yellow, often looks orange
RESET = "\033[0m"

# Extract PII entities
response = client.recognize_pii_entities(documents=documents, language="en")
for doc in response:
    print(f"\n\033[92mPII entities in document {doc.id}:\033[0m")
    for entity in doc.entities:
        print(f" - {entity.text}: "
              f"{ORANGE}{entity.category} (confidence: {entity.confidence_score:.2f}){RESET}"
)