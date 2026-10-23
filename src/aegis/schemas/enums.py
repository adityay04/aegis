from enum import Enum


class Severity(str, Enum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class EvaluationStatus(str, Enum):
    PASS = "pass"
    FAIL = "fail"
    UNCERTAIN = "uncertain"
    ERROR = "error"


class TargetKind(str, Enum):
    MOCK = "mock"
    LOCAL_LLM = "local_llm"
    REMOTE_API = "remote_api"


class TestCategory(str, Enum):
    __test__ = False

    PROMPT_INJECTION = "prompt_injection"
    JAILBREAK = "jailbreak"
    DATA_EXFILTRATION = "data_exfiltration"
    TOXICITY = "toxicity"
    BIAS = "bias"
    HALLUCINATION = "hallucination"
    OTHER = "other"