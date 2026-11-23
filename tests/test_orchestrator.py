import pytest
from aegis.orchestrator import Orchestrator
from aegis.generators import TemplateGenerator
from aegis.targets import MockTarget
from aegis.evaluators import RuleBasedEvaluator


@pytest.fixture
def orchestrator():
    return Orchestrator(
        generator=TemplateGenerator(),
        target=MockTarget(),
        evaluator=RuleBasedEvaluator(),
    )


async def test_orchestrator_runs_single_iteration(orchestrator):
    result = await orchestrator.run_single_iteration()

    assert "test_case" in result
    assert "model_response" in result
    assert "evaluation" in result

    test_case = result["test_case"]
    response = result["model_response"]
    evaluation = result["evaluation"]

    assert test_case.id == response.test_case_id
    assert response.id == evaluation.model_response_id