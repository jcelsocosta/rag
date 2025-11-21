from abc import ABC, abstractmethod
from typing import List, Dict, Any

class AbstractSearchGuardrails(ABC):
    @abstractmethod
    def sanitize(self, message: str) -> bool:
        pass