from abc import ABC, abstractmethod
from aegis.schemas import Evaluation, Score

class BaseScorer(ABC):
    @abstractmethod
    async def score(self, evaluation: Evaluation) -> Score:
        pass