from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition, MCPTool

PROJECT_ENDPOINT = "<YOUR_PROJECT_ENDPOINT>"  #Example "https://ai-103-exam-resource.services.ai.azure.com/api/projects/ai-103-exam-project"

def main():
    
    # Create client for OpenAI
    with(
            DefaultAzureCredential() as credential,
            AIProjectClient(endpoint=PROJECT_ENDPOINT, credential=credential) as project_client,
            project_client.get_openai_client() as openai_client,
         ):
    
        # Initialize agent MCP tool
        mcp_tool = MCPTool(
            server_label="api-specs",
            server_url="https://learn.microsoft.com/api/mcp",
            require_approval="never"
        )

        # Create a new agent with the MCP tool
        agent = project_client.agents.create_version(
            agent_name="MyAgent",
            definition=PromptAgentDefinition(
                model="gpt-5.1",
                instructions="You are a helpful agent that can use MCP tools to assist users. "
                                "Use the available MCP tools to answer questions and perform tasks.",
                tools=[mcp_tool],
            ),
        )

        print(f"Agent created (id: {agent.id}, name: {agent.name}, version: {agent.version})")

        # Create a conversation thread
        conversation = openai_client.conversations.create()
        print(f"Created conversation (id: {conversation.id})")

        print("\nType your message (type 'exit' or 'quit' to end):")
        
        while True:
            user_input = input("You: ")
            if user_input.strip().lower() in ["exit", "quit"]:
                print("Exiting conversation.")
                break
            
            response = openai_client.responses.create(
                conversation=conversation.id,
                input=user_input,
                extra_body={"agent_reference": {"name": agent.name, "type": "agent_reference"}},
            )
            print(f"Agent: {response.output_text}\n")

if __name__ == "__main__":
    main()