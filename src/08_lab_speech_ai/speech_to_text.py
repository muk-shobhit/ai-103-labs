from openai import AzureOpenAI
from pathlib import Path
from dotenv import load_dotenv
import os
load_dotenv()

FOUNDRY_SPEECH_PROJECT_ENDPOINT = os.getenv("FOUNDRY_SPEECH_PROJECT_ENDPOINT")
FOUNDRY_SPEECH_MODEL_KEY = os.getenv("FOUNDRY_SPEECH_MODEL_KEY")
FOUNDRY_SPEECH_API_VERSION = os.getenv("FOUNDRY_SPEECH_API_VERSION")
FOUNDRY_SPEECH_MODEL_DEPLOYMENT = os.getenv("FOUNDRY_SPEECH_MODEL_DEPLOYMENT")
    
# Create the Azure OpenAI client using project endpoint
client = AzureOpenAI(
    azure_endpoint=FOUNDRY_SPEECH_PROJECT_ENDPOINT,
    api_key=FOUNDRY_SPEECH_MODEL_KEY,
    api_version=FOUNDRY_SPEECH_API_VERSION
    )

# Get the audio file
file_path = Path("speech.wav")
audio_file = open(file_path, "rb")

# Use the model to transcribe the audio file
transcription = client.audio.transcriptions.create(
    model=FOUNDRY_SPEECH_MODEL_DEPLOYMENT,
    file=audio_file,
    response_format="text"
)

print(transcription)