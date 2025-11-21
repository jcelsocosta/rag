from abc import ABC, abstractmethod
from typing import List, Dict, Any

class AbstractDataIngestionRepository(ABC):
    @abstractmethod
    async def insert(self, vector_id: str, vector: List[float], payload: Dict[str, Any]):
        pass