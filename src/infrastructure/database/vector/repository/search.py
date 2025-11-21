from src.domain.usecase.repository.search import AbstractSearchRepository
from typing import List, Dict, Any
from ..settings import client

class SearchRepository(AbstractSearchRepository):
    _collection_name = "data"

    async def find_similarity(self, vector: List[float], limit: int, with_payload: bool):
        result = client.search(
            collection_name=self._collection_name,
            query_vector=vector,
            limit=limit,
            with_payload=with_payload,
        )
        return result