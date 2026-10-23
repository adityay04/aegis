import time
import uuid
import httpx

from aegis.schemas import ModelResponse, TestCase
from aegis.targets.base import BaseTarget


class LocalLLMTarget(BaseTarget):
    """Connects to a local model via an OpenAI-compatible API."""

    def __init__(
        self,
        target_id: str = "local-llm-001",
        model_name: str = "llama3",
        base_url: str = "http://localhost:11434/v1",
    ):
        self.target_id = target_id
        self.model_name = model_name
        self.base_url = base_url

    async def execute(self, test_case: TestCase) -> ModelResponse:
        start_time = time.perf_counter()
        
        url = f"{self.base_url}/chat/completions"
        headers = {"Content-Type": "application/json"}
        payload = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": test_case.prompt}],
            "temperature": 0.7,
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload, timeout=30.0)
                response.raise_for_status()
                
                data = response.json()
                content = data["choices"][0]["message"]["content"]
                
                latency_ms = (time.perf_counter() - start_time) * 1000
                
                return ModelResponse(
                    id=f"resp-{uuid.uuid4().hex[:8]}",
                    test_case_id=test_case.id,
                    target_id=self.target_id,
                    content=content,
                    latency_ms=latency_ms,
                    raw=data,
                )

        except Exception as e:
            latency_ms = (time.perf_counter() - start_time) * 1000
            return ModelResponse(
                id=f"resp-{uuid.uuid4().hex[:8]}",
                test_case_id=test_case.id,
                target_id=self.target_id,
                content=None,
                error=str(e),
                latency_ms=latency_ms,
            )