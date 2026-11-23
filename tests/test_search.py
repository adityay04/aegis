import pytest
from aegis.orchestrator import Orchestrator
from aegis.generators import TemplateGenerator
from aegis.targets import MockTarget
from aegis.evaluators import RuleBasedEvaluator
from aegis.scoring import WeightedScorer
from aegis.memory import InMemoryStore
from aegis.mutators import SimpleMutator
from aegis.search import AdaptiveSearcher
from aegis.schemas import (
    IterationResult, TestCase, ModelResponse, Evaluation, Score,
    EvaluationStatus, Severity, TestCategory
)


@pytest.fixture
def searcher():
    orchestrator = Orchestrator(
        generator=TemplateGenerator(),
        target=MockTarget(),
        evaluator=RuleBasedEvaluator(),
        scorer=WeightedScorer(),
    )
    memory = InMemoryStore()
    mutator = SimpleMutator()
    generator = TemplateGenerator()
    
    return AdaptiveSearcher(
        orchestrator=orchestrator,
        memory=memory,
        mutator=mutator,
        generator=generator,
        score_threshold=0.5
    )


@pytest.fixture
def high_scoring_result():
    test_case = TestCase(id="tc-high", name="High Score", prompt="Bad prompt", category=TestCategory.JAILBREAK)
    response = ModelResponse(id="resp-1", test_case_id="tc-high", target_id="mock", content="Bad response")
    evaluation = Evaluation(
        id="eval-1", test_case_id="tc-high", model_response_id="resp-1",
        status=EvaluationStatus.FAIL, severity=Severity.CRITICAL, confidence=1.0, evaluator="test"
    )
    score = Score(
        id="score-1", evaluation_id="eval-1",
        severity=1.0, confidence=1.0, novelty=0.5, reproducibility=0.5,
        strategy_effectiveness=0.5, total=0.9
    )
    return IterationResult(
        test_case=test_case, model_response=response, evaluation=evaluation, score=score
    )


async def test_adaptive_searcher_cold_start(searcher):
    result = await searcher.search()
    
    assert result.test_case is not None
    assert "parent_id" not in result.test_case.metadata
    assert len(searcher.memory.get_all()) == 1


async def test_adaptive_searcher_mutates_high_scores(searcher, high_scoring_result):
    searcher.memory.save(high_scoring_result)
    
    assert len(searcher.memory.get_all()) == 1

    result = await searcher.search()
    
    assert len(searcher.memory.get_all()) == 2
    assert "parent_id" in result.test_case.metadata
    assert result.test_case.metadata["parent_id"] == "tc-high"