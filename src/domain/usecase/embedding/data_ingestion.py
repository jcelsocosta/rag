from abc import ABC, abstractmethod
from typing import List

class AbstractDataIngestionEmbedding(ABC):
    @abstractmethod
    def generate_vector(self, target: str) -> List[float]:
        pass