import pytest
from aegis.schemas import Evaluation, EvaluationStatus, Severity
from aegis.scoring import WeightedScorer


@pytest.fixture
def sample_evaluation():
    return Evaluation(
        id="eval-123",
        test_case_id="tc-123",
        model_response_id="resp-123",
        status=EvaluationStatus.FAIL,
        severity=Severity.HIGH,
        confidence=0.9,
        evaluator="Test"
    )


async def test_weighted_scorer(sample_evaluation):
    scorer = WeightedScorer()
    score = await scorer.score(sample_evaluation)

    assert score.evaluation_id == sample_evaluation.id
    assert score.severity == 0.75
    assert score.confidence == 0.9
    assert score.total > 0