from aegis.generators import BaseGenerator
from aegis.targets import BaseTarget
from aegis.evaluators import BaseEvaluator
from aegis.scoring import BaseScorer
from aegis.schemas import IterationResult


class Orchestrator:
    def __init__(
        self,
        generator: BaseGenerator,
        target: BaseTarget,
        evaluator: BaseEvaluator,
        scorer: BaseScorer,
    ):
        self.generator = generator
        self.target = target
        self.evaluator = evaluator
        self.scorer = scorer

    async def run_single_iteration(self) -> IterationResult:
        test_case = await self.generator.generate()
        response = await self.target.execute(test_case)
        evaluation = await self.evaluator.evaluate(test_case, response)
        score = await self.scorer.score(evaluation)

        return IterationResult(
            test_case=test_case,
            model_response=response,
            evaluation=evaluation,
            score=score,
        )