import pytest
from aegis.orchestrator import Orchestrator
from aegis.generators import TemplateGenerator
from aegis.targets import MockTarget
from aegis.evaluators import RuleBasedEvaluator
from aegis.scoring import WeightedScorer
from aegis.experiment import ExperimentRunner
from aegis.memory import InMemoryStore
from aegis.schemas import ExperimentConfig


@pytest.fixture
def runner():
    orchestrator = Orchestrator(
        generator=TemplateGenerator(),
        target=MockTarget(),
        evaluator=RuleBasedEvaluator(),
        scorer=WeightedScorer(),
    )
    memory = InMemoryStore()
    return ExperimentRunner(orchestrator, memory)


async def test_experiment_runner_executes_multiple_iterations(runner):
    config = ExperimentConfig(
        id="exp-001",
        name="First Automated Experiment",
        iterations=3
    )

    result = await runner.run(config)

    assert result.config.id == "exp-001"
    assert result.config.iterations == 3
    assert len(result.results) == 3
    
    for iteration in result.results:
        assert iteration.test_case is not None
        assert iteration.score.total >= 0.0
        
    assert len(runner.memory.get_all()) == 3