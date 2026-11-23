from aegis.orchestrator import Orchestrator
from aegis.schemas import ExperimentConfig, ExperimentResult
from aegis.memory import BaseMemory

class ExperimentRunner:
    def __init__(self, orchestrator: Orchestrator, memory: BaseMemory):
        self.orchestrator = orchestrator
        self.memory = memory

    async def run(self, config: ExperimentConfig) -> ExperimentResult:
        results = []

        for _ in range(config.iterations):
            iteration_result = await self.orchestrator.run_single_iteration()
            self.memory.save(iteration_result)
            results.append(iteration_result)

        return ExperimentResult(
            config=config,
            results=results
        )