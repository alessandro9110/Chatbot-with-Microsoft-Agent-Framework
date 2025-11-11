from azure.cosmos import CosmosClient, PartitionKey
from azure.cosmos.exceptions import CosmosResourceNotFoundError
import json
from typing import List, Dict, Any, Optional
from config import Config

class CosmosDBClient:
    def __init__(self):
        self.client = CosmosClient(Config.COSMOS_ENDPOINT, Config.COSMOS_KEY)
        self.database = self.client.get_database_client(Config.COSMOS_DATABASE)
        self.container = self.database.get_container_client(Config.COSMOS_CONTAINER)

    async def save_conversation(self, user_id: str, conversation_id: str, messages: List[Dict[str, Any]]) -> None:
        """Save conversation to Cosmos DB with user_id as partition key."""
        item = {
            "id": conversation_id,
            "user_id": user_id,
            "messages": messages,
            "last_updated": str(datetime.utcnow().isoformat())
        }
        await self.container.upsert_item(item)

    async def get_conversation(self, user_id: str, conversation_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve conversation from Cosmos DB."""
        try:
            item = await self.container.read_item(conversation_id, partition_key=user_id)
            return item
        except CosmosResourceNotFoundError:
            return None

    async def get_user_conversations(self, user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent conversations for a user."""
        query = f"SELECT * FROM c WHERE c.user_id = @user_id ORDER BY c.last_updated DESC OFFSET 0 LIMIT {limit}"
        parameters = [{"name": "@user_id", "value": user_id}]
        items = list(self.container.query_items(query=query, parameters=parameters))
        return items

    async def delete_conversation(self, user_id: str, conversation_id: str) -> None:
        """Delete a conversation."""
        await self.container.delete_item(conversation_id, partition_key=user_id)