import warnings
warnings.simplefilter("ignore")

import asyncio
import os

from agent_framework import Agent, tool
from agent_framework.foundry import FoundryChatClient
from agent_framework.orchestrations import MagenticBuilder
from azure.identity import AzureCliCredential
from dotenv import load_dotenv

load_dotenv()

client = FoundryChatClient(
        project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
        model=os.environ["FOUNDRY_MODEL"],
        credential=AzureCliCredential(),
    )

researcher = Agent(
        name="Researcher",
        description="Finds information",
        instructions="""
        Find key facts about the topic.
        Keep the response short.
        """,
        client=client,
    )

writer = Agent(
        name="Writer",
        description="Creates final answer",
        instructions="""
        Create a concise final answer
        using information from the researcher.
        """,
        client=client,
    )

manager = Agent(
        name="Manager",
        description="Coordinates agents",
        instructions="""
        Delegate work to the team and
        provide the final answer.
        """,
        client=client,
    )

async def main() -> None:
    workflow = (
            MagenticBuilder(participants=[researcher,writer,],
                intermediate_output_from=[
                    researcher,
                    writer,
                ],
                manager_agent=manager,
                max_round_count=5,
            )
            .build()
        )

    task = "What is Azure AI Foundry?"

    print(f"\nTask: {task}\n")

    events = [
            event
            async for event in workflow.run(task,stream=True)
        ]

    print("\nResponses:\n")

    for event in events:
            if event.type == "intermediate":
                if hasattr(event.data, "messages"):
                    for msg in event.data.messages:
                        if getattr(msg, "text", None):
                            print(
                                f"{event.executor_id}: "
                                f"{msg.text}\n"
                            )
            elif event.type == "output":
                print("\nFinal Answer:\n")
                for msg in event.data:
                    print(
                        f"{msg.author_name or msg.role}: "
                        f"{msg.text}\n"
                    )

if __name__ == "__main__":
    asyncio.run(main())