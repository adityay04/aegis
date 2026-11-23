from typing import List
from aegis.schemas import IterationResult, TestCategory
from aegis.memory.base import BaseMemory

class InMemoryStore(BaseMemory):
    def __init__(self):
        self.results: List[IterationResult] = []

    def save(self, result: IterationResult) -> None:
        self.results.append(result)

    def get_all(self) -> List[IterationResult]:
        return self.results

    def get_by_category(self, category: TestCategory) -> List[IterationResult]:
        return [r for r in self.results if r.test_case.category == category]

    def get_high_scoring(self, min_score: float) -> List[IterationResult]:
        return [r for r in self.results if r.score.total >= min_score]