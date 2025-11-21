from abc import ABC, abstractmethod
from typing import List

class AbstractDataIngestionTransformer(ABC):
    @abstractmethod
    def generate_chunks(self, full_text: str) -> List[str]:
        pass