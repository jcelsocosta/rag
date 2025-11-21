from abc import ABC, abstractmethod
from typing import List

class AbstractSearchRepository(ABC):
    @abstractmethod
    async def find_similarity(self, vector: List[float], limit: int, with_payload: bool):
        pass
