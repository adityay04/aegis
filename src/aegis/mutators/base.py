from abc import ABC, abstractmethod
from aegis.schemas import TestCase

class BaseMutator(ABC):
    @abstractmethod
    async def mutate(self, test_case: TestCase) -> TestCase:
        pass