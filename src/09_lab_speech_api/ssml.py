from pathlib import Path
from dotenv import load_dotenv
import os
import azure.cognitiveservices.speech as speech_sdk
load_dotenv()

FOUNDRY_RESOURCE_ENDPOINT =os.getenv("FOUNDRY_RESOURCE_ENDPOINT")
FOUNDRY_PROJECT_KEY = os.getenv("FOUNDRY_PROJECT_KEY")

speech_config = speech_sdk.SpeechConfig(subscription=FOUNDRY_PROJECT_KEY, endpoint=FOUNDRY_RESOURCE_ENDPOINT)

audio_config = speech_sdk.audio.AudioOutputConfig(use_default_speaker=True)

# Use speech synthesizer to synthesize text as speech
speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

ssml = (
    """
    <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">
        <voice name="en-US-AriaNeural">
            Hello, how are you today?
        </voice>
        <voice name="en-US-GuyNeural">
            I'm doing great. Thanks for asking!
        </voice>
    </speak>
    """
)

speech_synthesis_result = speech_synthesizer.speak_ssml_async(ssml).get()

# Did it succeeed?
if speech_synthesis_result.reason == speech_sdk.ResultReason.SynthesizingAudioCompleted:
    print("Speech synthesized for ssml [{}]".format(ssml))

elif speech_synthesis_result.reason == speech_sdk.ResultReason.Canceled:
    cancellation_details = speech_synthesis_result.cancellation_details
    print("Speech synthesis canceled: {}".format(cancellation_details.reason))
 
    if cancellation_details.reason == speech_sdk.CancellationReason.Error:
        if cancellation_details.error_details:
            print("Error details: {}".format(cancellation_details.error_details))