from pathlib import Path
from dotenv import load_dotenv
import os
import azure.cognitiveservices.speech as speech_sdk
load_dotenv()

FOUNDRY_RESOURCE_ENDPOINT =os.getenv("FOUNDRY_RESOURCE_ENDPOINT")
FOUNDRY_PROJECT_KEY = os.getenv("FOUNDRY_PROJECT_KEY")

speech_config = speech_sdk.SpeechConfig(subscription=FOUNDRY_PROJECT_KEY, endpoint=FOUNDRY_RESOURCE_ENDPOINT)

speech_config.set_speech_synthesis_output_format(speech_sdk.SpeechSynthesisOutputFormat.Riff16Khz16BitMonoPcm)
speech_config.speech_synthesis_voice_name='en-US-Brian:DragonHDLatestNeural'

audio_config = speech_sdk.audio.AudioOutputConfig(use_default_speaker=True)

# Use speech synthesizer to synthesize text as speech
speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
text = """
        I am speaking with the Brian voice! I hope you like it. 
        This is so cool! I can say whatever I want with this voice! I am loving it!"
       """

speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

# Did it succeeed?
if speech_synthesis_result.reason == speech_sdk.ResultReason.SynthesizingAudioCompleted:
    print("Speech synthesized for text [{}]".format(text))

elif speech_synthesis_result.reason == speech_sdk.ResultReason.Canceled:
    cancellation_details = speech_synthesis_result.cancellation_details
    print("Speech synthesis canceled: {}".format(cancellation_details.reason))
 
    if cancellation_details.reason == speech_sdk.CancellationReason.Error:
        if cancellation_details.error_details:
            print("Error details: {}".format(cancellation_details.error_details))