from typing import List
from pydantic import Field
from .base import AegisBaseModel
from .test_case import TestCase
from .model_response import ModelResponse
from .evaluation import Evaluation
from .score import Score

class IterationResult(AegisBaseModel):
    test_case: TestCase
    model_response: ModelResponse
    evaluation: Evaluation
    score: Score

class ExperimentConfig(AegisBaseModel):
    id: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    iterations: int = Field(..., gt=0)

class ExperimentResult(AegisBaseModel):
    config: ExperimentConfig
    results: List[IterationResult]