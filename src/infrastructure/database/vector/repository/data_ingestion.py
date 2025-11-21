from src.domain.usecase.repository.data_ingestion import AbstractDataIngestionRepository
from typing import List, Dict, Any
from ..settings import client

class DataIngestionRepository(AbstractDataIngestionRepository):
    _collection_name = "data"

    async def insert(self, vector_id: str, vector: List[float], payload: Dict[str, Any]):
        client.upsert(
            collection_name=self._collection_name,
            points=[
                {
                    "id": str(vector_id),
                    "vector": vector,
                    "payload": payload
                }
            ]
        )