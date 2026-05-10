from dotenv import load_dotenv
import os
import sys
import json
from azure.ai.contentunderstanding import ContentUnderstandingClient
from azure.core.credentials import AzureKeyCredential

def main(): 
    try: 
        load_dotenv()
        FOUNDRY_ENDPOINT = os.getenv("FOUNDRY_RESOURCE_ENDPOINT")
        FOUNDRY_KEY = os.getenv("FOUNDRY_PROJECT_KEY")
        ANALYZER_NAME = os.getenv("ANALYZER_NAME")
        
        # Create a Content Understanding analyzer
        print(f"Creating {ANALYZER_NAME}")

        # Create the Content Understanding client
        client = ContentUnderstandingClient(
            endpoint=FOUNDRY_ENDPOINT,
            credential=AzureKeyCredential(FOUNDRY_KEY)
        )

        ##############################  Create Analyzer  ####################################

        # Parse the schema JSON into a ContentAnalyzer object
        with open("biz-card.json", "r") as file:
            schema_json = json.load(file)
        
        schema = json.dumps(schema_json)

        analyzer_definition = json.loads(schema)

        # Create the analyzer using the SDK (long-running operation)
        poller = client.begin_create_analyzer(
            analyzer_id=ANALYZER_NAME,
            resource=analyzer_definition,
            allow_replace=True
        )

        # Wait for the operation to complete
        result = poller.result()
        print(f"Analyzer '{ANALYZER_NAME}' created successfully.")
        print(f"Status: {result['status'] if isinstance(result, dict) else 'Succeeded'}")   
        
        ##############################  Read insights using Analyzer  ####################################
        
        # Use Content Understanding to analyze the image
        image_file = 'biz-card-1.png'
        print(f"Analyzing {image_file}")

        # Read the image data
        with open(image_file, "rb") as file:
            image_data = file.read()

        # Submit the image for analysis
        print("Submitting request...")
        poller = client.begin_analyze_binary(
            analyzer_id=ANALYZER_NAME,
            binary_input=image_data
        )

        # Wait for the analysis to complete
        result = poller.result()
        print("Analysis succeeded:\n")

        # Save JSON results to a file
        output_file = "results.json"
        with open(output_file, "w") as json_file:
            json.dump(dict(result), json_file, indent=4, default=str)
            print(f"Response saved in {output_file}\n")

        # Iterate through the contents and extract fields
        for content in result.contents:
            if hasattr(content, 'fields') and content.fields:
                for field_name, field_data in content.fields.items():
                    value = field_data.value if hasattr(field_data, 'value') else None
                    print(f"{field_name}: {value}")
        
    except Exception as ex:
                print(ex)

if __name__ == '__main__':
    main()