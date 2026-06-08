import math

from app.core.config import (
    BETA,
    CONTEXT_CROWDING_SHARE,
    CROWDING_ALPHA,
    DIST_MAX_M,
    FLOOR_COST_MULTIPLIER,
    POLICY_BLEND,
    PURPOSE_WEIGHTS,
)


REC_FEATURE_KEYS: tuple[str, ...] = ("deg", "dist", "purpose", "seat", "crowding")


def compute_fixed_weights(crowding: str, purpose: str) -> dict[str, float]:
    deg_weight = CROWDING_ALPHA[crowding]
    context_total = max(1.0 - deg_weight - BETA, 0.0)
    crowding_weight = context_total * CONTEXT_CROWDING_SHARE
    purpose_seat_total = context_total - crowding_weight
    purpose_seat_weights = PURPOSE_WEIGHTS[purpose]

    return {
        "deg": deg_weight,
        "dist": BETA,
        "purpose": purpose_seat_total * purpose_seat_weights["purpose"],
        "seat": purpose_seat_total * purpose_seat_weights["seat"],
        "crowding": crowding_weight,
    }


def blend_weights(
    fixed_weights: dict[str, float],
    learned_weights: dict[str, float] | None = None,
) -> dict[str, float]:
    if learned_weights is None or POLICY_BLEND <= 0.0:
        return dict(fixed_weights)

    return {
        key: (1.0 - POLICY_BLEND) * fixed_weights[key] + POLICY_BLEND * learned_weights[key]
        for key in REC_FEATURE_KEYS
    }


def compute_rec_score(
    deg_score: float,
    dist_norm: float,
    purpose_score: float,
    seat_score: float,
    crowding_score: float,
    crowding: str,
    purpose: str,
    learned_weights: dict[str, float] | None = None,
) -> float:
    weights = blend_weights(compute_fixed_weights(crowding, purpose), learned_weights)
    return round(
        weights["deg"] * (1.0 - deg_score)
        + weights["dist"] * (1.0 - dist_norm)
        + weights["purpose"] * purpose_score
        + weights["seat"] * seat_score
        + weights["crowding"] * crowding_score,
        4,
    )


def compute_dist_norm(
    user_lat: float,
    user_lng: float,
    place_lat: float,
    place_lng: float,
    floor_m: float = 0.0,
) -> float:
    R = 6_371_000.0
    lat1 = math.radians(user_lat)
    lat2 = math.radians(place_lat)
    dlat = math.radians(place_lat - user_lat)
    dlng = math.radians(place_lng - user_lng)
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlng / 2) ** 2
    dist_m = R * 2 * math.asin(math.sqrt(a)) + floor_m * FLOOR_COST_MULTIPLIER
    return round(min(dist_m / DIST_MAX_M, 1.0), 4)
