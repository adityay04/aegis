import uuid
from aegis.schemas import TestCase, ModelResponse, Evaluation, EvaluationStatus
from aegis.evaluators.base import BaseEvaluator


class SelfHealingEvaluator(BaseEvaluator):
    def __init__(self, evaluator: BaseEvaluator, confidence_threshold: float = 0.7, max_retries: int = 3):
        self.evaluator = evaluator
        self.confidence_threshold = confidence_threshold
        self.max_retries = max_retries

    async def evaluate(self, test_case: TestCase, response: ModelResponse) -> Evaluation:
        best_eval = await self.evaluator.evaluate(test_case, response)

        if best_eval.status != EvaluationStatus.UNCERTAIN and best_eval.confidence >= self.confidence_threshold:
            return best_eval

        for _ in range(self.max_retries):
            new_eval = await self.evaluator.evaluate(test_case, response)
            
            if new_eval.status != EvaluationStatus.UNCERTAIN and new_eval.confidence >= self.confidence_threshold:
                return new_eval.model_copy(update={
                    "id": f"eval-{uuid.uuid4().hex[:8]}",
                    "metadata": {**new_eval.metadata, "healed": "true"}
                })
            
            if new_eval.confidence > best_eval.confidence:
                best_eval = new_eval

        return best_eval.model_copy(update={
            "id": f"eval-{uuid.uuid4().hex[:8]}",
            "metadata": {**best_eval.metadata, "quarantined": "true"},
            "reasoning": f"Quarantined after {self.max_retries} retries. Original: {best_eval.reasoning}"
        })