import asyncio
import os
from typing import cast
import warnings
warnings.simplefilter("ignore")
from agent_framework import Agent, AgentResponse, Message
from agent_framework.foundry import FoundryChatClient
from agent_framework.orchestrations import SequentialBuilder
from azure.identity import AzureCliCredential
from dotenv import load_dotenv

load_dotenv()

async def main() -> None:
    client = FoundryChatClient(
        project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
        model=os.environ["FOUNDRY_MODEL"],
        credential=AzureCliCredential(),
    )

    writer = Agent(
        client=client,
        instructions=("You are a concise copywriter. Provide a single, punchy marketing sentence based on the prompt."),
        name="writer",
    )

    reviewer = Agent(
        client=client,
        instructions=("You are a thoughtful reviewer. Give brief feedback on the previous assistant message."),
        name="reviewer",
    )

    workflow = SequentialBuilder(participants=[writer, reviewer], output_from="all").build()

    prompt = "Write a tagline for a budget-friendly eBike."
    result = await workflow.run(prompt)
    conversation = [Message(role="user", contents=[prompt])]
   
    for output in result.get_outputs():
        response = cast(AgentResponse, output)
        conversation.extend(response.messages)

    if conversation:
        print("===== Final Conversation =====")
        for i, msg in enumerate(conversation, start=1):
            name = msg.author_name or ("assistant" if msg.role == "assistant" else "user")
            print(f"{'-' * 60}\n\n{i:02d} [{name}]\n\n{msg.text}\n")

if __name__ == "__main__":
    asyncio.run(main())