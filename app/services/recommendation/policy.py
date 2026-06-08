from app.core.config import ETA, REC_INITIAL_WEIGHTS

_rec_weights: dict[str, float] = dict(REC_INITIAL_WEIGHTS)


def get_weights() -> dict[str, float]:
    return dict(_rec_weights)


def update_policy(
    reward: float,
    deg_score: float,
    dist_norm: float,
    purpose_score: float,
    seat_score: float,
    crowding_score: float,
) -> None:
    global _rec_weights

    gradients = {
        "deg": 1.0 - deg_score,
        "dist": 1.0 - dist_norm,
        "purpose": purpose_score,
        "seat": seat_score,
        "crowding": crowding_score,
    }

    updated = {k: _rec_weights[k] + ETA * reward * gradients[k] for k in _rec_weights}

    # Clip to [0, ∞) then renormalise to sum = 1
    clipped = {k: max(v, 0.0) for k, v in updated.items()}
    total = sum(clipped.values())
    if total == 0.0:
        _rec_weights = dict(REC_INITIAL_WEIGHTS)
    else:
        _rec_weights = {k: v / total for k, v in clipped.items()}
