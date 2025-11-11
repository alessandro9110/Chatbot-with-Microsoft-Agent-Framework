import asyncio
import os
from typing import List, Dict, Any
from datetime import datetime

from agent_framework import ChatAgent, ChatMessage, Role
from agent_framework.azure import AzureAIAgentClient
from agent_framework import HostedWebSearchTool, HostedFileSearchTool, HostedVectorStoreContent
from azure.identity.aio import AzureCliCredential

from config import Config
from cosmos_client import CosmosDBClient
from ai_search_client import AISearchClient

class ChatbotAgent:
    def __init__(self):
        Config.validate()
        self.cosmos_client = CosmosDBClient()
        self.ai_search_client = AISearchClient()
        self.credential = AzureCliCredential()

    async def create_agent(self) -> ChatAgent:
        """Create the Azure AI Agent with tools."""
        # Create Azure AI Agent Client
        agent_client = AzureAIAgentClient(async_credential=self.credential)

        # Define tools
        tools = [
            HostedWebSearchTool(
                name="WebSearch",
                description="Search the web for current information"
            ),
            # Add file search tool if vector store is available
            # HostedFileSearchTool(inputs=[HostedVectorStoreContent(vector_store_id="your-vector-store-id")])
        ]

        # Create the agent
        agent = await agent_client.create_agent(
            name="ChatbotAgent",
            instructions="""
            You are a helpful chatbot that can search for information and maintain conversation history.
            Use the available tools to provide accurate and up-to-date information.
            Always be polite and helpful.
            """,
            tools=tools,
            model=Config.AZURE_AI_MODEL_DEPLOYMENT_NAME
        )

        return ChatAgent(
            chat_client=agent_client,
            instructions="You are a helpful assistant with access to web search and conversation history.",
            tools=tools
        )

    async def chat(self, user_id: str, message: str, conversation_id: Optional[str] = None) -> str:
        """Handle a chat interaction."""
        # Create or get conversation ID
        if not conversation_id:
            conversation_id = f"conv_{user_id}_{int(datetime.utcnow().timestamp())}"

        # Get conversation history
        conversation = await self.cosmos_client.get_conversation(user_id, conversation_id)
        messages = conversation.get("messages", []) if conversation else []

        # Add user message
        messages.append({
            "role": "user",
            "content": message,
            "timestamp": str(datetime.utcnow().isoformat())
        })

        # Create agent and run
        agent = await self.create_agent()
        chat_messages = [ChatMessage(role=Role(msg["role"]), content=msg["content"]) for msg in messages]

        response = await agent.run(message, conversation_id=conversation_id)

        # Add assistant response
        messages.append({
            "role": "assistant",
            "content": response.text,
            "timestamp": str(datetime.utcnow().isoformat())
        })

        # Save updated conversation
        await self.cosmos_client.save_conversation(user_id, conversation_id, messages)

        return response.text

async def main():
    """Main function for testing the chatbot."""
    chatbot = ChatbotAgent()

    # Example usage
    user_id = "test_user"
    response = await chatbot.chat(user_id, "Hello, can you search for the latest news about AI?")
    print(f"Response: {response}")

if __name__ == "__main__":
    asyncio.run(main())