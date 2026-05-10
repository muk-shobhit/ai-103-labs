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
translation_cfg.add_target_language('hi')

# Configure speech synthesis
speech_cfg = speech_sdk.SpeechConfig(subscription=FOUNDRY_PROJECT_KEY, 
                                     endpoint=FOUNDRY_TRANSLATE_PROJECT_ENDPOINT)

audio_cfg = speech_sdk.audio.AudioOutputConfig(use_default_speaker=True)
voices = {
        "fr": "fr-FR-HenriNeural",
        "hi": "hi-IN-SwaraNeural",
}

# Get trsnslations
translator = speech_sdk.translation.TranslationRecognizer(translation_config=translation_cfg,
                                                          audio_config=audio_cfg)
print("Speak now...")
translation_results = translator.recognize_once_async().get()
print(f"Translating '{translation_results.text}'")


# process the translation results
translations = translation_results.translations
for translation_language in translations:

    # Print ressults
    print(f"{translation_language}: '{translations[translation_language]}'")

    speech_cfg.speech_synthesis_voice_name = voices.get(translation_language)
 
    speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_cfg, audio_cfg)
    speak = speech_synthesizer.speak_text_async(translations[translation_language]).get()
