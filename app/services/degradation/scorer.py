from app.core.config import DEG_GOOD_THRESHOLD, DEG_POOR_THRESHOLD
from app.schemas.wifi_input import WifiMeasurement
from app.schemas.degradation_output import DegradationResult
from app.services.degradation.ewmv import METRICS
from app.services.degradation.normalizer import normalize
from app.services.degradation.weight_manager import (
    get_or_init_state,
    save_state,
    update_weights,
)

# Latest deg_score per location — consumed by Layer 2
_latest_deg_scores: dict[str, float] = {}


def get_latest_deg_score(location: str) -> float:
    return _latest_deg_scores.get(location, 0.5)


def _deg_level(score: float) -> str:
    if score < DEG_GOOD_THRESHOLD:
        return "Good"
    if score < DEG_POOR_THRESHOLD:
        return "Fair"
    return "Poor"


def compute_deg_score(measurement: WifiMeasurement) -> DegradationResult:
    """
    Layer 1 entry point: IoT measurement → deg_score aggregated feature.

    deg_score = Σ w(i) · μ(i)  over 7 metrics ∈ [0, 1]

    μ(i) is the EMA of metric i stored in EWMVState.mu. Using μ instead of
    the raw normalised value provides temporal smoothing — a single noisy
    measurement does not immediately spike deg_score. download/upload absent
    (None) leave their μ unchanged (carry-forward inside update_ewmv).
    """
    norm = normalize(measurement)

    state = get_or_init_state(measurement.location)
    state = update_weights(state, norm)
    save_state(measurement.location, state)

    w = state.w
    mu = state.ewmv_state.mu
    deg_score = sum(w[m] * mu[m] for m in METRICS)

    _latest_deg_scores[measurement.location] = deg_score

    return DegradationResult(
        location=measurement.location,
        timestamp=measurement.timestamp,
        deg_score=round(deg_score, 6),
        level=_deg_level(deg_score),
    )


def batch_compute_deg_scores(measurements: list[WifiMeasurement]) -> list[DegradationResult]:
    """
    65분 주기 슬라이딩 윈도우 배치 처리.

    N개 측정값을 시간순으로 순차 처리해 EWMV 가중치를 재보정한다.
    각 측정값에 대한 DegradationResult를 동일 순서로 반환하며,
    마지막 결과(results[-1])가 해당 장소의 최신 deg_score다.
    Spring Boot는 results[-1]을 Firebase deg_results/{location}/latest에 저장한다.
    """
    return [compute_deg_score(m) for m in measurements]
