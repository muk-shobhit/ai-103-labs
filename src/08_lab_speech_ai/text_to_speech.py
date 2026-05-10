from openai import AzureOpenAI
from pathlib import Path
from dotenv import load_dotenv
import os
load_dotenv()

FOUNDRY_SPEECH_PROJECT_ENDPOINT = os.getenv("FOUNDRY_SPEECH_PROJECT_ENDPOINT")
FOUNDRY_SPEECH_MODEL_KEY = os.getenv("FOUNDRY_SPEECH_MODEL_KEY")
FOUNDRY_SPEECH_API_VERSION = os.getenv("FOUNDRY_SPEECH_API_VERSION")
FOUNDRY_TEXT_TO_SPEECH_MODEL_DEPLOYMENT = os.getenv("FOUNDRY_TEXT_TO_SPEECH_MODEL_DEPLOYMENT")

# Create the Azure OpenAI client using project endpoint
client = AzureOpenAI(
    azure_endpoint=FOUNDRY_SPEECH_PROJECT_ENDPOINT,
    api_key=FOUNDRY_SPEECH_MODEL_KEY,
    api_version=FOUNDRY_SPEECH_API_VERSION
    )

# Path for audio output file
speech_file_path = Path("output_speech.wav")

# Generate speech and save to file
with client.audio.speech.with_streaming_response.create(
            model=FOUNDRY_TEXT_TO_SPEECH_MODEL_DEPLOYMENT,
            voice="alloy",
            input="This speech was AI-g+enerated! Isn't that amazing? Let's explore the world of AI together and see what we can create!",
            instructions="Speak in an upbeat, excited tone.",
    ) as response:
    response.stream_to_file(speech_file_path)

print(f"Speech generated and saved to {speech_file_path}")