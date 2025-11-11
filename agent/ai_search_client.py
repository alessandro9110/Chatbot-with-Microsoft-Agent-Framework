from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery
from azure.core.credentials import AzureKeyCredential
from typing import List, Dict, Any
import json
from config import Config

class AISearchClient:
    def __init__(self):
        self.client = SearchClient(
            endpoint=Config.AI_SEARCH_ENDPOINT,
            index_name=Config.AI_SEARCH_INDEX,
            credential=AzureKeyCredential(Config.AI_SEARCH_KEY)
        )

    async def search_vector(self, query: str, vector: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        """Perform vector search in Azure AI Search."""
        vector_query = VectorizedQuery(vector=vector, k_nearest_neighbors=top_k, fields="content_vector")
        results = self.client.search(
            search_text=query,
            vector_queries=[vector_query],
            select=["content", "title", "metadata"],
            top=top_k
        )
        return [result for result in results]

    async def search_hybrid(self, query: str, vector: List[float], top_k: int = 5) -> List[Dict[str, Any]]:
        """Perform hybrid search (text + vector)."""
        vector_query = VectorizedQuery(vector=vector, k_nearest_neighbors=top_k, fields="content_vector")
        results = self.client.search(
            search_text=query,
            vector_queries=[vector_query],
            select=["content", "title", "metadata"],
            top=top_k,
            query_type="semantic"
        )
        return [result for result in results]