from aegis.orchestrator import Orchestrator
from aegis.memory import BaseMemory
from aegis.mutators import BaseMutator
from aegis.generators import BaseGenerator
from aegis.search.base import BaseSearcher
from aegis.schemas import IterationResult


class AdaptiveSearcher(BaseSearcher):
    def __init__(
        self,
        orchestrator: Orchestrator,
        memory: BaseMemory,
        mutator: BaseMutator,
        generator: BaseGenerator,
        score_threshold: float = 0.7,
    ):
        self.orchestrator = orchestrator
        self.memory = memory
        self.mutator = mutator
        self.generator = generator
        self.score_threshold = score_threshold

    async def search(self) -> IterationResult:
        high_scoring_results = self.memory.get_high_scoring(self.score_threshold)

        if high_scoring_results:
            best_result = max(high_scoring_results, key=lambda x: x.score.total)
            test_case = await self.mutator.mutate(best_result.test_case)
        else:
            test_case = await self.generator.generate()

        result = await self.orchestrator.run_test_case(test_case)
        self.memory.save(result)
        
        return result