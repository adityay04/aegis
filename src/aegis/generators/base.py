from abc import ABC, abstractmethod
from aegis.schemas import TestCase

class BaseGenerator(ABC):
    @abstractmethod
    async def generate(self) -> TestCase:
        pass