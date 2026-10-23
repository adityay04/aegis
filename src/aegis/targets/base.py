from abc import ABC, abstractmethod
from aegis.schemas import TestCase, ModelResponse

class BaseTarget(ABC):
    """Abstract interface for all AEGIS targets."""

    @abstractmethod
    async def execute(self, test_case: TestCase) -> ModelResponse:
        """
        Send a TestCase to the target model and return a standardized ModelResponse.
        Must measure latency and catch errors gracefully.
        """
        pass