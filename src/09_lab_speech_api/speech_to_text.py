from pathlib import Path
from dotenv import load_dotenv
import os
import azure.cognitiveservices.speech as speech_sdk
load_dotenv()

FOUNDRY_RESOURCE_ENDPOINT =os.getenv("FOUNDRY_RESOURCE_ENDPOINT")
FOUNDRY_PROJECT_KEY = os.getenv("FOUNDRY_PROJECT_KEY")

speech_config = speech_sdk.SpeechConfig(    
    subscription=FOUNDRY_PROJECT_KEY,
    endpoint=FOUNDRY_RESOURCE_ENDPOINT)

# Audio config determines the audio stream source (defaults to system mic)
file_path = Path(__file__).parent / "speech.wav"

audio_config = speech_sdk.audio.AudioConfig(filename=str(file_path))

# Use a speech recognizer to transcribe the audio
speech_recognizer = speech_sdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

result = speech_recognizer.recognize_once_async().get()

if result.reason == speech_sdk.ResultReason.RecognizedSpeech:
    print(f"Transcription:\n{result.text}")
else:
    print("Error transcribing message: {}".format(result.reason))