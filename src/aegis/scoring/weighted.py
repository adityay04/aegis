import uuid
from aegis.schemas import Evaluation, Score, Severity
from aegis.scoring.base import BaseScorer

class WeightedScorer(BaseScorer):
    def __init__(self):
        self.severity_map = {
            Severity.INFO: 0.0,
            Severity.LOW: 0.25,
            Severity.MEDIUM: 0.5,
            Severity.HIGH: 0.75,
            Severity.CRITICAL: 1.0
        }

    async def score(self, evaluation: Evaluation) -> Score:
        sev_val = self.severity_map.get(evaluation.severity, 0.0)
        conf_val = evaluation.confidence
        novelty = 0.5
        repro = 0.5
        strat_eff = 0.5
        
        total = (sev_val * 0.4) + (conf_val * 0.3) + (novelty * 0.1) + (repro * 0.1) + (strat_eff * 0.1)
        total = max(0.0, min(1.0, total))

        return Score(
            id=f"score-{uuid.uuid4().hex[:8]}",
            evaluation_id=evaluation.id,
            severity=sev_val,
            confidence=conf_val,
            novelty=novelty,
            reproducibility=repro,
            strategy_effectiveness=strat_eff,
            total=total
        )