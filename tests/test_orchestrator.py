import pytest
from aegis.orchestrator import Orchestrator
from aegis.generators import TemplateGenerator
from aegis.targets import MockTarget
from aegis.evaluators import RuleBasedEvaluator
from aegis.scoring import WeightedScorer


@pytest.fixture
def orchestrator():
    return Orchestrator(
        generator=TemplateGenerator(),
        target=MockTarget(),
        evaluator=RuleBasedEvaluator(),
        scorer=WeightedScorer(),
    )


async def test_orchestrator_runs_single_iteration(orchestrator):
    result = await orchestrator.run_single_iteration()

    assert result.test_case.id == result.model_response.test_case_id
    assert result.model_response.id == result.evaluation.model_response_id
    assert result.evaluation.id == result.score.evaluation_id