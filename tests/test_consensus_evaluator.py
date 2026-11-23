import pytest
from aegis.evaluators import ConsensusEvaluator, BaseEvaluator
from aegis.schemas import (
    TestCase, ModelResponse, Evaluation, EvaluationStatus, Severity
)


class MockPassEvaluator(BaseEvaluator):
    async def evaluate(self, test_case: TestCase, response: ModelResponse) -> Evaluation:
        return Evaluation(
            id="eval-pass", test_case_id=test_case.id, model_response_id=response.id,
            status=EvaluationStatus.PASS, severity=Severity.INFO, confidence=1.0, evaluator="MockPass"
        )

class MockFailEvaluator(BaseEvaluator):
    async def evaluate(self, test_case: TestCase, response: ModelResponse) -> Evaluation:
        return Evaluation(
            id="eval-fail", test_case_id=test_case.id, model_response_id=response.id,
            status=EvaluationStatus.FAIL, severity=Severity.HIGH, confidence=1.0, evaluator="MockFail"
        )


@pytest.fixture
def sample_data():
    tc = TestCase(id="tc-1", name="test", prompt="prompt")
    resp = ModelResponse(id="resp-1", test_case_id="tc-1", target_id="mock", content="response")
    return tc, resp


async def test_consensus_evaluator_agreement(sample_data):
    tc, resp = sample_data
    evaluator = ConsensusEvaluator(evaluators=[MockPassEvaluator(), MockPassEvaluator()])
    result = await evaluator.evaluate(tc, resp)

    assert result.status == EvaluationStatus.PASS
    assert result.confidence == 1.0
    assert "Consensus reached" in result.reasoning


async def test_consensus_evaluator_disagreement(sample_data):
    tc, resp = sample_data
    evaluator = ConsensusEvaluator(evaluators=[MockPassEvaluator(), MockFailEvaluator()])
    result = await evaluator.evaluate(tc, resp)

    assert result.status == EvaluationStatus.UNCERTAIN
    assert result.confidence == 0.5
    assert "Evaluator disagreement detected" in result.reasoning