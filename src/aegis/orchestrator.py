from aegis.generators import BaseGenerator
from aegis.targets import BaseTarget
from aegis.evaluators import BaseEvaluator


class Orchestrator:
    def __init__(
        self,
        generator: BaseGenerator,
        target: BaseTarget,
        evaluator: BaseEvaluator,
    ):
        self.generator = generator
        self.target = target
        self.evaluator = evaluator

    async def run_single_iteration(self) -> dict:
        test_case = await self.generator.generate()
        response = await self.target.execute(test_case)
        evaluation = await self.evaluator.evaluate(test_case, response)

        return {
            "test_case": test_case,
            "model_response": response,
            "evaluation": evaluation,
        }