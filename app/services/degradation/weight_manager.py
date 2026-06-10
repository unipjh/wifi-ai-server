import math
from dataclasses import dataclass, field

from app.core.config import ALPHA, LAMBDA_, INITIAL_WEIGHTS
from app.services.degradation.ewmv import (
    EWMVState,
    METRICS,
    initial_ewmv_state,
    update_ewmv,
)


@dataclass
class WeightState:
    w: dict[str, float] = field(
        default_factory=lambda: dict(INITIAL_WEIGHTS)
    )
    ewmv_state: EWMVState = field(default_factory=EWMVState)


# Per-zone weight state — keyed by zone_id
_zone_states: dict[str, WeightState] = {}


def get_or_init_state(zone_id: str) -> WeightState:
    if zone_id not in _zone_states:
        _zone_states[zone_id] = WeightState(
            ewmv_state=initial_ewmv_state(zone_id),
        )
    return _zone_states[zone_id]


def save_state(zone_id: str, state: WeightState) -> None:
    _zone_states[zone_id] = state


def _softmax(values: list[float]) -> list[float]:
    # Subtract max for numerical stability before exp
    max_v = max(values)
    exps = [math.exp(v - max_v) for v in values]
    total = sum(exps)
    return [e / total for e in exps]


def update_weights(state: WeightState, x: dict[str, float]) -> WeightState:
    """
    Update EWMV state then recompute adaptive weights.

    Step 3 from degradation_principle.md:
      w(i,t) = (w0(i) + λ·Softmax(σ²(i,t))) / Σ_j(w0(j) + λ·Softmax(σ²(j,t)))

    Metrics with higher variance get larger weight — they are currently
    more unstable and thus more informative about network degradation.
    """
    new_ewmv = update_ewmv(state.ewmv_state, x, ALPHA)

    variances = [new_ewmv.var[m] for m in METRICS]
    softmax_vars = _softmax(variances)

    w0 = INITIAL_WEIGHTS
    raw = {
        m: w0[m] + LAMBDA_ * softmax_vars[i]
        for i, m in enumerate(METRICS)
    }
    total = sum(raw.values())
    new_w = {m: v / total for m, v in raw.items()}

    return WeightState(w=new_w, ewmv_state=new_ewmv)
