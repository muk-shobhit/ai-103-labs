import warnings
warnings.simplefilter("ignore")
import asyncio
import os
from typing import cast
from agent_framework import (Agent, AgentResponseUpdate,Message)
from agent_framework.foundry import FoundryChatClient
from agent_framework.orchestrations import GroupChatBuilder, GroupChatState
from azure.identity import AzureCliCredential
from dotenv import load_dotenv

load_dotenv()

def round_robin_selector(state: GroupChatState) -> str:
    """A round-robin selector function that picks the next speaker based on the current round index."""

    participant_names = list(state.participants.keys())
    return participant_names[state.current_round % len(participant_names)]


async def main() -> None:
    # Create a Responses client using Azure OpenAI and Azure CLI credentials for all agents
    client = FoundryChatClient(
        project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
        model=os.environ["FOUNDRY_MODEL"],
        credential=AzureCliCredential(),
    )

    # Participant agents
    expert = Agent(
        name="PythonExpert",
        instructions=(
            "You are an expert in Python in a workgroup. "
            "Your job is to answer Python related questions and refine your answer "
            "based on feedback from all the other participants."
            "Keep you answer concise and to the point, and avoid unnecessary jargon. max two lines per response."
        ),
        client=client,
    )

    verifier = Agent(
        name="AnswerVerifier",
        instructions=(
            "You are a programming expert in a workgroup. "
            f"Your job is to review the answer provided by {expert.name} and point "
            "out statements that are technically true but practically dangerous."
            "If there is nothing woth pointing out, respond with 'The answer looks good to me.'"
            "Keep you answer concise and to the point, and avoid unnecessary jargon. max two lines per response."
        ),
        client=client,
    )

    clarifier = Agent(
        name="AnswerClarifier",
        instructions=(
            "You are an accessibility expert in a workgroup. "
            f"Your job is to review the answer provided by {expert.name} and point "
            "out jargons or complex terms that may be difficult for a beginner to understand."
            "If there is nothing worth pointing out, respond with 'The answer looks clear to me.'"
            "Keep you answer concise and to the point, and avoid unnecessary jargon. max two lines per response."
        ),
        client=client,
    )

    skeptic = Agent(
        name="Skeptic",
        instructions=(
            "You are a devil's advocate in a workgroup. "
            f"Your job is to review the answer provided by {expert.name} and point "
            "out caveats, exceptions, and alternative perspectives."
            "If there is nothing worth pointing out, respond with 'I have no further questions.'"
            "Keep you answer concise and to the point, and avoid unnecessary jargon. max two lines per response."
        ),
        client=client,
    )

    workflow = (
        GroupChatBuilder(
            participants=[expert, verifier, clarifier, skeptic],
            termination_condition=lambda conversation: len(conversation) >= 6,
            intermediate_output_from=[expert, verifier, clarifier, skeptic],
            selection_func=round_robin_selector,
        )
        .with_termination_condition(lambda conversation: len(conversation) >= 6)
        .build()
    )

    task = "How does Python’s Protocol differ from abstract base classes?"

    print("\nStarting Group Chat with round-robin speaker selector...\n")
    print(f"TASK: {task}\n")
    print("=" * 80)

    last_response_id: str | None = None
    async for event in workflow.run(task, stream=True):
        if event.type in ("intermediate", "output"):
            data = event.data
            if isinstance(data, AgentResponseUpdate):
                rid = data.response_id
                if rid != last_response_id:
                    if last_response_id is not None:
                        print("\n")
                    print(f"\033[92m{data.author_name}:\033[0m", end=" ", flush=True)
                    last_response_id = rid
                print(data.text, end="", flush=True)
            elif event.type == "output":
                # The output of the group chat workflow is a collection of chat messages from all participants
                outputs = cast(list[Message], event.data)
                print("\n" + "=" * 80)
                print("\nFinal Conversation Transcript:\n")
                for message in outputs:
                    print(f"{message.author_name or message.role}: {message.text}\n")


if __name__ == "__main__":
    asyncio.run(main())