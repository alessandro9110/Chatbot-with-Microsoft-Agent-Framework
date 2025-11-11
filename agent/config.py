import os
from typing import Optional

class Config:
    # Azure AI Foundry
    AZURE_AI_PROJECT_ENDPOINT: str = os.getenv("AZURE_AI_PROJECT_ENDPOINT", "")
    AZURE_AI_MODEL_DEPLOYMENT_NAME: str = os.getenv("AZURE_AI_MODEL_DEPLOYMENT_NAME", "")

    # Cosmos DB
    COSMOS_ENDPOINT: str = os.getenv("COSMOS_ENDPOINT", "")
    COSMOS_KEY: str = os.getenv("COSMOS_KEY", "")
    COSMOS_DATABASE: str = os.getenv("COSMOS_DATABASE", "chatbot-db")
    COSMOS_CONTAINER: str = os.getenv("COSMOS_CONTAINER", "conversations")

    # Azure AI Search
    AI_SEARCH_ENDPOINT: str = os.getenv("AI_SEARCH_ENDPOINT", "")
    AI_SEARCH_KEY: str = os.getenv("AI_SEARCH_KEY", "")
    AI_SEARCH_INDEX: str = os.getenv("AI_SEARCH_INDEX", "knowledge-base")

    @classmethod
    def validate(cls) -> None:
        required = [
            ("AZURE_AI_PROJECT_ENDPOINT", cls.AZURE_AI_PROJECT_ENDPOINT),
            ("AZURE_AI_MODEL_DEPLOYMENT_NAME", cls.AZURE_AI_MODEL_DEPLOYMENT_NAME),
            ("COSMOS_ENDPOINT", cls.COSMOS_ENDPOINT),
            ("COSMOS_KEY", cls.COSMOS_KEY),
            ("AI_SEARCH_ENDPOINT", cls.AI_SEARCH_ENDPOINT),
            ("AI_SEARCH_KEY", cls.AI_SEARCH_KEY),
        ]
        missing = [name for name, value in required if not value]
        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")