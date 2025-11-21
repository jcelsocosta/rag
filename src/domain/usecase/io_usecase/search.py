from dataclasses import dataclass
from typing import List, Dict

@dataclass
class SearchUseCaseInput:
    message: str

@dataclass
class SearchUseCaseOutput:
    answer: str
    citations: List[str]
    metrics: Dict[str, int]