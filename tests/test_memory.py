import pytest
from aegis.memory import InMemoryStore, SQLiteMemory
from aegis.schemas import (
    IterationResult, TestCase, ModelResponse, Evaluation, Score,
    EvaluationStatus, Severity, TestCategory
)

@pytest.fixture
def sample_result():
    test_case = TestCase(id="tc-1", name="Test", prompt="Prompt", category=TestCategory.JAILBREAK)
    response = ModelResponse(id="resp-1", test_case_id="tc-1", target_id="mock", content="Hello")
    evaluation = Evaluation(
        id="eval-1", test_case_id="tc-1", model_response_id="resp-1",
        status=EvaluationStatus.FAIL, severity=Severity.HIGH, confidence=0.9, evaluator="test"
    )
    score = Score(
        id="score-1", evaluation_id="eval-1",
        severity=0.75, confidence=0.9, novelty=0.5, reproducibility=0.5,
        strategy_effectiveness=0.5, total=0.85
    )
    return IterationResult(
        test_case=test_case, model_response=response, evaluation=evaluation, score=score
    )

def test_in_memory_save_and_get(sample_result):
    memory = InMemoryStore()
    memory.save(sample_result)
    
    assert len(memory.get_all()) == 1
    assert memory.get_all()[0].test_case.id == "tc-1"

def test_in_memory_filter_by_category(sample_result):
    memory = InMemoryStore()
    memory.save(sample_result)

    jailbreak_results = memory.get_by_category(TestCategory.JAILBREAK)
    tox_results = memory.get_by_category(TestCategory.TOXICITY)

    assert len(jailbreak_results) == 1
    assert len(tox_results) == 0

def test_in_memory_filter_by_score(sample_result):
    memory = InMemoryStore()
    memory.save(sample_result)

    high_scores = memory.get_high_scoring(0.8)
    low_scores = memory.get_high_scoring(0.9)

    assert len(high_scores) == 1
    assert len(low_scores) == 0

def test_sqlite_memory_save_and_get(sample_result):
    memory = SQLiteMemory()
    memory.save(sample_result)
    
    assert len(memory.get_all()) == 1
    assert memory.get_all()[0].test_case.id == "tc-1"

def test_sqlite_memory_filter_by_category(sample_result):
    memory = SQLiteMemory()
    memory.save(sample_result)

    jailbreak_results = memory.get_by_category(TestCategory.JAILBREAK)
    tox_results = memory.get_by_category(TestCategory.TOXICITY)

    assert len(jailbreak_results) == 1
    assert len(tox_results) == 0

def test_sqlite_memory_filter_by_score(sample_result):
    memory = SQLiteMemory()
    memory.save(sample_result)

    high_scores = memory.get_high_scoring(0.8)
    low_scores = memory.get_high_scoring(0.9)

    assert len(high_scores) == 1
    assert len(low_scores) == 0