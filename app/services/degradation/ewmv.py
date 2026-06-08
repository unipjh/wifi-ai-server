from dataclasses import dataclass, field

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
