from abc import ABC, abstractmethod
from aegis.schemas import IterationResult

class BaseSearcher(ABC):
    @abstractmethod
    async def search(self) -> IterationResult:
        pass