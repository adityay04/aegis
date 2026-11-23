import uuid
from typing import List
from collections import Counter
from aegis.schemas import TestCase, ModelResponse, Evaluation, EvaluationStatus, Severity
from aegis.evaluators.base import BaseEvaluator


class ConsensusEvaluator(BaseEvaluator):
    def __init__(self, evaluators: List[BaseEvaluator], agreement_threshold: float = 0.66):
        self.evaluators = evaluators
        self.agreement_threshold = agreement_threshold

    async def evaluate(self, test_case: TestCase, response: ModelResponse) -> Evaluation:
        results = []
        for evaluator in self.evaluators:
            res = await evaluator.evaluate(test_case, response)
            results.append(res)

        if not results:
            raise ValueError("No evaluators provided to ConsensusEvaluator")

        status_counts = Counter(r.status for r in results)
        most_common_status, count = status_counts.most_common(1)[0]
        agreement_ratio = count / len(results)

        if agreement_ratio >= self.agreement_threshold:
            best_result = next(r for r in results if r.status == most_common_status)
            return best_result.model_copy(update={
                "id": f"eval-{uuid.uuid4().hex[:8]}",
                "confidence": agreement_ratio,
                "evaluator": "ConsensusEvaluator",
                "reasoning": f"Consensus reached ({agreement_ratio*100:.1f}% agreement). Original reasoning: {best_result.reasoning}"
            })
        
        return Evaluation(
            id=f"eval-{uuid.uuid4().hex[:8]}",
            test_case_id=test_case.id,
            model_response_id=response.id,
            status=EvaluationStatus.UNCERTAIN,
            severity=Severity.MEDIUM,
            confidence=agreement_ratio,
            reasoning=f"Evaluator disagreement detected. Statuses: {dict(status_counts)}",
            evaluator="ConsensusEvaluator"
        )