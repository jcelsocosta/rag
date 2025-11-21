from abc import ABC, abstractmethod
from typing import List, Dict

class AbstractDataIngestionCommon(ABC):
    @abstractmethod
    def read_folder(self, path: str) -> List[Dict[str, str]]:
        pass