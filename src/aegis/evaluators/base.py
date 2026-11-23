from abc import ABC, abstractmethod
from aegis.schemas import TestCase, ModelResponse, Evaluation

class BaseEvaluator(ABC):
    """Abstract interface for all AEGIS evaluators."""

    @abstractmethod
    async def evaluate(self, test_case: TestCase, response: ModelResponse) -> Evaluation:
        """
        Analyze the ModelResponse against the TestCase and return an Evaluation.
        """
        pass