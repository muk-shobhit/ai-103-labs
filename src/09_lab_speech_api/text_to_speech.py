from pathlib import Path
from dotenv import load_dotenv
import os
import azure.cognitiveservices.speech as speech_sdk
load_dotenv()

FOUNDRY_RESOURCE_ENDPOINT =os.getenv("FOUNDRY_RESOURCE_ENDPOINT")
FOUNDRY_PROJECT_KEY = os.getenv("FOUNDRY_PROJECT_KEY")

speech_config = speech_sdk.SpeechConfig(subscription=FOUNDRY_PROJECT_KEY, endpoint=FOUNDRY_RESOURCE_ENDPOINT)

audio_config = speech_sdk.audio.AudioOutputConfig(use_default_speaker=True)

speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
text = """
        Ohh! It's so nice to meet you! I am talking to you through Azure Cognitive Services 
        Text to Speech API! I hope you are having a great day!
       """

speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

if speech_synthesis_result.reason == speech_sdk.ResultReason.SynthesizingAudioCompleted:
    print("Speech synthesized for text [{}]".format(text))

elif speech_synthesis_result.reason == speech_sdk.ResultReason.Canceled:
    cancellation_details = speech_synthesis_result.cancellation_details
    print("Speech synthesis canceled: {}".format(cancellation_details.reason))