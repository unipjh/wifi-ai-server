from dataclasses import dataclass, field

from app.core.config import (
    INITIAL_STATS,
    NORM_MAX,
    RSSI_BEST,
    RSSI_WORST,
    _DEFAULT_STAT,
)

# Must match keys in INITIAL_WEIGHTS and normalizer output
# 모든 키는 API 필드명과 동일하게 유지
METRICS: tuple[str, ...] = (
    "rssi",
    "ping_gw", "jitter_gw", "packet_loss_gw",
    "ping_ext", "jitter_ext", "packet_loss_ext",
    "download_mbps", "upload_mbps",
)


@dataclass
class EWMVState:
    # μ(i, t-1): per-metric exponential moving average
    mu: dict[str, float] = field(
        default_factory=lambda: {m: 0.5 for m in METRICS}
    )
    # σ²(i, t-1): per-metric exponentially weighted moving variance
    var: dict[str, float] = field(
        default_factory=lambda: {m: 0.0 for m in METRICS}
    )


def _clamp01(value: float) -> float:
    return max(0.0, min(value, 1.0))


def _normalize_stat_mean(metric: str, raw_mean: float) -> float:
    if metric == "rssi":
        rssi_range = RSSI_BEST - RSSI_WORST
        return 1.0 - _clamp01((raw_mean - RSSI_WORST) / rssi_range)

    if metric in ("download_mbps", "upload_mbps"):
        return 1.0 - _clamp01(raw_mean / NORM_MAX[metric])

    return _clamp01(raw_mean / NORM_MAX[metric])


def _normalize_stat_var(metric: str, raw_std: float) -> float:
    if metric == "rssi":
        denom = RSSI_BEST - RSSI_WORST
    else:
        denom = NORM_MAX[metric]

    normalized_std = _clamp01(raw_std / denom)
    return normalized_std ** 2


def initial_ewmv_state(location: str) -> EWMVState:
    """Build a location-specific EWMV prior from collected raw statistics."""
    stats = INITIAL_STATS.get(location, _DEFAULT_STAT())
    return EWMVState(
        mu={
            metric: _normalize_stat_mean(metric, stats[metric]["mean"])
            for metric in METRICS
        },
        var={
            metric: _normalize_stat_var(metric, stats[metric]["std"])
            for metric in METRICS
        },
    )


def update_ewmv(state: EWMVState, x: dict[str, float], alpha: float) -> EWMVState:
    """
    One-step EMA + EWMV update.

    Step 1 — EMA:  μ(i,t) = α·x(i,t) + (1-α)·μ(i,t-1)
    Step 2 — EWMV: σ²(i,t) = α·σ²(i,t-1) + (1-α)·(x(i,t) - μ(i,t-1))²

    Metrics absent from x (periodic measurements arriving as null) are
    carried forward unchanged — their EWMV state is not updated this step.
    """
    new_mu: dict[str, float] = {}
    new_var: dict[str, float] = {}

    for m in METRICS:
        if m not in x:
            new_mu[m] = state.mu[m]
            new_var[m] = state.var[m]
            continue
        prev_mu = state.mu[m]
        new_mu[m] = alpha * x[m] + (1 - alpha) * prev_mu
        new_var[m] = alpha * state.var[m] + (1 - alpha) * (x[m] - prev_mu) ** 2

    return EWMVState(mu=new_mu, var=new_var)
