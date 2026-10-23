import asyncio
import time
import uuid

from aegis.schemas import ModelResponse, TestCase
from aegis.targets.base import BaseTarget

class MockTarget(BaseTarget):
    """A deterministic target for testing the pipeline without an actual LLM."""

    def __init__(self, target_id: str = "mock-001"):
        self.target_id = target_id

    async def execute(self, test_case: TestCase) -> ModelResponse:
        start_time = time.perf_counter()

        await asyncio.sleep(0.1)

        fake_content = f"[MOCK RESPONSE] I received: '{test_case.prompt}'"

        latency_ms = (time.perf_counter() - start_time) * 1000

        return ModelResponse(
            id=f"resp-{uuid.uuid4().hex[:8]}",
            test_case_id=test_case.id,
            target_id=self.target_id,
            content=fake_content,
            latency_ms=latency_ms,
            raw={"mock": True}
        )