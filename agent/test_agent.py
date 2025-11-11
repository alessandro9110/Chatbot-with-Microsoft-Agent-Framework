import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock
from agent.main import ChatbotAgent
from agent.config import Config

@pytest.fixture
def mock_config():
    """Mock configuration for testing."""
    Config.AZURE_AI_PROJECT_ENDPOINT = "https://test.azure.com"
    Config.AZURE_AI_MODEL_DEPLOYMENT_NAME = "gpt-4o"
    Config.COSMOS_ENDPOINT = "https://test.cosmos.azure.com"
    Config.COSMOS_KEY = "test-key"
    Config.AI_SEARCH_ENDPOINT = "https://test.search.windows.net"
    Config.AI_SEARCH_KEY = "test-key"

@pytest.mark.asyncio
async def test_chatbot_agent_creation(mock_config):
    """Test ChatbotAgent initialization."""
    agent = ChatbotAgent()
    assert agent.cosmos_client is not None
    assert agent.ai_search_client is not None
    assert agent.credential is not None

@pytest.mark.asyncio
async def test_chat_interaction(mock_config):
    """Test basic chat interaction."""
    agent = ChatbotAgent()

    # Mock the agent creation and response
    with unittest.mock.patch.object(agent, 'create_agent', new_callable=AsyncMock) as mock_create:
        mock_agent = AsyncMock()
        mock_agent.run.return_value = MagicMock(text="Test response")
        mock_create.return_value = mock_agent

        response = await agent.chat("test_user", "Hello")
        assert response == "Test response"
        mock_agent.run.assert_called_once()