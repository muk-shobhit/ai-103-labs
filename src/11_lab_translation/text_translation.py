from azure.ai.translation.text import *
from azure.ai.translation.text.models import InputTextItem
from azure.identity import DefaultAzureCredential
import os
from dotenv import load_dotenv

load_dotenv()

FOUNDRY_TRANSLATE_PROJECT_ENDPOINT = os.environ.get("FOUNDRY_TRANSLATE_PROJECT_ENDPOINT")

credential = DefaultAzureCredential()

client = TextTranslationClient(credential=credential, endpoint=FOUNDRY_TRANSLATE_PROJECT_ENDPOINT)

input_text_elements = [InputTextItem(text="I love this course ")]

translation_results = client.translate(body=input_text_elements, to_language=["fr", "hi"])
index = 0

for translation in translation_results:
    input_text = input_text_elements[index].text
    index += 1
    
    sourceLanguage = translation.detected_language
    
    for translated_text in translation.translations:
        print(f"\n'{input_text}' was translated from {sourceLanguage.language} to {translated_text.to} as '{translated_text.text}'.\n")
