import os
from urllib.request import urlopen, Request
import base64
from pathlib import Path
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import OpenAI

def main(): 
    try: 
        load_dotenv()
        FOUNDRY_ENDPOINT = "<YOUR_FOUNDRY_ENDPOINT>"  #Example "https://ai-103-exam-resource.services.ai.azure.com/providers/blackforestlabs/v1/flux-2-pro?api-version=preview"
        FOUNDRY_MODEL = "FLUX.2-pro"
        
        token_provider = get_bearer_token_provider(DefaultAzureCredential(), "https://ai.azure.com/.default")

        client = OpenAI(
            base_url=FOUNDRY_ENDPOINT,
            api_key=token_provider
        )
        
        # Generate an image
        img_results = client.images.generate(
            model=FOUNDRY_MODEL,
            prompt="A Man on beach chilling",
            n=1,
            size="1024x1024",
        )

        # Save the generated image
        image_data = base64.b64decode(img_results.data[0].b64_json)
        
        with open("image.png", "wb") as image_file:
            image_file.write(image_data)

    except Exception as ex:
        print(ex)


if __name__ == '__main__':
    main()