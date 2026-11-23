import pytest
from aegis.evaluators import SelfHealingEvaluator, BaseEvaluator
from aegis.schemas import (
    TestCase, ModelResponse, Evaluation, EvaluationStatus, Severity
)


class FlakyEvaluator(BaseEvaluator):
    def __init__(self):
        self.calls = 0

    async def evaluate(self, test_case: TestCase, response: ModelResponse) -> Evaluation:
        self.calls += 1
        if self.calls == 1:
            return Evaluation(
                id="eval-1", test_case_id=test_case.id, model_response_id=response.id,
                status=EvaluationStatus.UNCERTAIN, severity=Severity.MEDIUM, confidence=0.4, evaluator="Flaky"
            )
        return Evaluation(
            id="eval-2", test_case_id=test_case.id, model_response_id=response.id,
            status=EvaluationStatus.PASS, severity=Severity.INFO, confidence=0.9, evaluator="Flaky"
        )


class BrokenEvaluator(BaseEvaluator):
    async def evaluate(self, test_case: TestCase, response: ModelResponse) -> Evaluation:
        return Evaluation(
            id="eval-3", test_case_id=test_case.id, model_response_id=response.id,
            status=EvaluationStatus.UNCERTAIN, severity=Severity.MEDIUM, confidence=0.3, evaluator="Broken"
        )


@pytest.fixture
def sample_data():
    tc = TestCase(id="tc-1", name="test", prompt="prompt")
    resp = ModelResponse(id="resp-1", test_case_id="tc-1", target_id="mock", content="response")
    return tc, resp


async def test_self_healing_evaluator_success(sample_data):
    tc, resp = sample_data
    flaky = FlakyEvaluator()
    healer = SelfHealingEvaluator(evaluator=flaky)
    
    result = await healer.evaluate(tc, resp)
    
    assert result.status == EvaluationStatus.PASS
    assert result.confidence == 0.9
    assert result.metadata["healed"] == "true"
    assert flaky.calls == 2


async def test_self_healing_evaluator_quarantine(sample_data):
    tc, resp = sample_data
    broken = BrokenEvaluator()
    healer = SelfHealingEvaluator(evaluator=broken, max_retries=2)
    
    result = await healer.evaluate(tc, resp)
    
    assert result.status == EvaluationStatus.UNCERTAIN
    assert result.metadata["quarantined"] == "true"
    assert "Quarantined after 2 retries" in result.reasoning