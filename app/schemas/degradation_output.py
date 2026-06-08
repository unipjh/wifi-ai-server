from pydantic import BaseModel


class DegradationResult(BaseModel):
    location:  str
    timestamp: str    # ISO 8601, +09:00 오프셋 포함
    deg_score: float  # ∈ [0, 1] — 0=최상, 1=최악
    level:     str    # "Good" | "Fair" | "Poor"
