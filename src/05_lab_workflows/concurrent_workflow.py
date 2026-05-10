import warnings
warnings.simplefilter("ignore")
import asyncio
import os
from typing import Any
from agent_framework import Agent, Message
from agent_framework.foundry import FoundryChatClient
from agent_framework.orchestrations import ConcurrentBuilder
from azure.identity import AzureCliCredential
from dotenv import load_dotenv

load_dotenv()

async def main() -> None:
    client = FoundryChatClient(
        project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
        model=os.environ["FOUNDRY_MODEL"],
        credential=AzureCliCredential(),
    )

    researcher = Agent(
        client=client,
        instructions=(
            "You're an expert market and product researcher. Given a prompt, provide concise, factual insights,"
            " opportunities, and risks."
        ),
        name="researcher",
    )

    marketer = Agent(
        client=client,
        instructions=(
            "You're a creative marketing strategist. Craft compelling value propositions and target messaging"
            " aligned to the prompt."
        ),
        name="marketer",
    )

    legal = Agent(
        client=client,
        instructions=(
            "You're a cautious legal/compliance reviewer. Highlight constraints, disclaimers, and policy concerns"
            " based on the prompt."
        ),
        name="legal",
    )

    workflow = ConcurrentBuilder(participants=[researcher, marketer, legal]).build()

    events = await workflow.run("We are launching a new budget-friendly electric bike for urban commuters.")
    outputs = events.get_outputs()

    if outputs:
        print("===== Final Aggregated Conversation (messages) =====")
       
        for output in outputs:
            for i, msg in enumerate(output.messages, start=1):
                print(f"\n{i:02d} [{msg.author_name}]:")
                print(msg.text)
                
    else:
        print("No outputs received from the workflow.")
        
if __name__ == "__main__":
    asyncio.run(main())            