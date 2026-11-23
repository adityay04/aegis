from abc import ABC, abstractmethod
from typing import List
from aegis.schemas import IterationResult, TestCategory

class BaseMemory(ABC):
    @abstractmethod
    def save(self, result: IterationResult) -> None:
        pass

    @abstractmethod
    def get_all(self) -> List[IterationResult]:
        pass

    @abstractmethod
    def get_by_category(self, category: TestCategory) -> List[IterationResult]:
        pass

    @abstractmethod
    def get_high_scoring(self, min_score: float) -> List[IterationResult]:
        pass