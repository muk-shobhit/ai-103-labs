import os
from urllib.request import urlopen, Request
import base64
from pathlib import Path
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import OpenAI
import time

def main(): 
    try: 
        load_dotenv()
        FOUNDRY_ENDPOINT = os.getenv("FOUNDRY_VIDEO_OPENAI_ENDPOINT")
        FOUNDRY_MODEL = "sora-2"
        
        token_provider = get_bearer_token_provider(DefaultAzureCredential(), "https://ai.azure.com/.default")

        client = OpenAI(
            base_url=FOUNDRY_ENDPOINT,
            api_key=token_provider
        )
        
        # Create the video generation job
        video = client.videos.create(
            model=FOUNDRY_MODEL,
            prompt="A cute smiling dog wearing a stylish outfit, walking down a city street, cinematic lighting with background relaxing music",
            size="1280x720",
            seconds="12",
        )

        print(f"Video creation started. ID: {video.id}")

        # Poll for completion
        while video.status not in ["completed", "failed", "cancelled"]:
            print(f"Status: {video.status}. Waiting...")
            time.sleep(20)
            video = client.videos.retrieve(video.id)

        # Download when complete
        if video.status == "completed":
            content = client.videos.download_content(video.id, variant="video")
            content.write_to_file("output.mp4")
            print("Video saved to output.mp4")
    
    except Exception as ex:
                print(ex)

if __name__ == '__main__':
    main()