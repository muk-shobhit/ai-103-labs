from azure.ai.translation.text import *
from azure.ai.translation.text.models import InputTextItem
from azure.identity import DefaultAzureCredential
import azure.cognitiveservices.speech as speech_sdk
import os
from dotenv import load_dotenv

load_dotenv()

FOUNDRY_TRANSLATE_PROJECT_ENDPOINT = os.environ.get("FOUNDRY_TRANSLATE_PROJECT_ENDPOINT")
FOUNDRY_PROJECT_KEY = os.environ.get("FOUNDRY_PROJECT_KEY")

translation_cfg = speech_sdk.translation.SpeechTranslationConfig(
                    subscription=FOUNDRY_PROJECT_KEY, endpoint=FOUNDRY_TRANSLATE_PROJECT_ENDPOINT)

translation_cfg.speech_recognition_language = 'en-US'
translation_cfg.add_target_language('fr')
translation_cfg.add_target_language('ja')
translation_cfg.add_target_language('hi')

print('Ready to translate from',translation_cfg.speech_recognition_language)

# Configure audio source
audio_cfg = speech_sdk.AudioConfig(use_default_microphone=True)

# Get a TranslationRecognizr object
translator = speech_sdk.translation.TranslationRecognizer(translation_config=translation_cfg, audio_config=audio_cfg)

# Get input from mic and translate
print("Speak now...")

translation_results = translator.recognize_once_async().get()

print(f"\nTranslating '{translation_results.text}'\n")

# Print each translation
translations = translation_results.translations
for translation_language in translations:
    print(f"{translation_language}: '{translations[translation_language]}'\n")