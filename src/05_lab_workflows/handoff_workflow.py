import warnings
warnings.simplefilter("ignore")
import asyncio
import os
from agent_framework import Agent, tool
from agent_framework.foundry import FoundryChatClient
from agent_framework.orchestrations import HandoffBuilder
from azure.identity import AzureCliCredential
from dotenv import load_dotenv

load_dotenv()

client = FoundryChatClient(
        project_endpoint=os.environ["FOUNDRY_PROJECT_ENDPOINT"],
        model=os.environ["FOUNDRY_MODEL"],
        credential=AzureCliCredential(),
    )

@tool(approval_mode="never_require")
def process_refund(order_number: str) -> str:
    """Simple demo tool that simulates a refund."""
    return f"Refund completed for order {order_number}."

triage_agent = Agent(
        name="triage",
        client=client,
        instructions="""
        You are a support triage agent.

        If the user asks for a refund,
        hand off to the customer service agent.
        """,
        require_per_service_call_history_persistence=True
    )

customer_service_agent = Agent(
    name="customer_service",
    client=client,
    instructions="""
    You are a customer service representative.

    When you receive a refund request:
    - Tell the user you have reviewed the request.
    - Hand off to refund.
    """,
    require_per_service_call_history_persistence=True
)

refund_agent = Agent(
        name="refund",
        client=client,
        instructions="""
        Process refund requests using the refund tool.
        """,
        tools=[process_refund],
        require_per_service_call_history_persistence=True
    )

async def main() -> None:
    
    workflow = (
        HandoffBuilder(
            name="refund_workflow",
            participants=[triage_agent, customer_service_agent, refund_agent],
        )
        .with_start_agent(triage_agent)
        .build()
    )

    prompt = "I need a refund for order 1234."
    print(f"\nTASK: {prompt}\n")

    events = await workflow.run(prompt)
    
    for event in events:
            if event.type == "handoff_sent":
                print(
                    f"{event.data.source} -> {event.data.target}"
                )

            elif event.type == "output":

                if hasattr(event.data, "messages"):
                    for msg in event.data.messages:
                        if getattr(msg, "text", None):
                            print(
                                f"\n {event.executor_id}: "
                                f"{msg.text}\n"
                            )
            

if __name__ == "__main__":
    asyncio.run(main())