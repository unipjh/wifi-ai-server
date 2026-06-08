from datetime import datetime, timedelta, timezone

from app.core.config import PURPOSE_WEIGHTS, SEAT_KEY
from app.services.recommendation.venue_profiles import AVAILABILITY, VENUE_PROFILE

_KST = timezone(timedelta(hours=9))


def get_time_slot(timestamp: str) -> str:
    dt = datetime.fromisoformat(timestamp).astimezone(_KST)
    prefix = "WE" if dt.weekday() >= 5 else "WD"
    h = dt.hour
    if 9 <= h < 12:        # 09:00–11:59
        suffix = "AM"
    elif 12 <= h < 18:    # 12:00–17:59
        suffix = "PEAK"
    elif 18 <= h < 22:    # 18:00–21:59
        suffix = "PM"
    else:                 # 22:00–08:59
        suffix = "NIGHT"
    return f"{prefix}_{suffix}"


def compute_ctx_score(location: str, purpose: str, seat: str) -> float:
    v = VENUE_PROFILE[location]
    p_score = v[f"p_{purpose.lower()}"]

    seat_key = SEAT_KEY[seat]
    s_score = (v["solo"] + v["team"]) / 2 if seat_key is None else v[seat_key]

    w = PURPOSE_WEIGHTS[purpose]
    return round(w["purpose"] * p_score + w["seat"] * s_score, 3)


def compute_purpose_score(location: str, purpose: str, timestamp: str) -> float:
    slot = get_time_slot(timestamp)
    availability = AVAILABILITY.get(location, {}).get(slot, 0.0)
    score = VENUE_PROFILE[location][f"p_{purpose.lower()}"]
    return round(score * availability, 4)


def compute_seat_score(location: str, seat: str, timestamp: str) -> float:
    slot = get_time_slot(timestamp)
    availability = AVAILABILITY.get(location, {}).get(slot, 0.0)
    v = VENUE_PROFILE[location]
    seat_key = SEAT_KEY[seat]
    score = (v["solo"] + v["team"]) / 2 if seat_key is None else v[seat_key]
    return round(score * availability, 4)


def compute_crowding_score(location: str, crowding: str, timestamp: str) -> float:
    slot = get_time_slot(timestamp)
    availability = AVAILABILITY.get(location, {}).get(slot, 0.0)
    quiet = VENUE_PROFILE[location]["quiet"]

    if crowding == "QUIET":
        score = quiet
    elif crowding == "LOUD_OK":
        score = 1.0 - quiet
    else:
        score = 0.5

    return round(score * availability, 4)


def compute_context_features(
    location: str,
    purpose: str,
    seat: str,
    crowding: str,
    timestamp: str,
) -> dict[str, float]:
    purpose_score = compute_purpose_score(location, purpose, timestamp)
    seat_score = compute_seat_score(location, seat, timestamp)
    crowding_score = compute_crowding_score(location, crowding, timestamp)
    ctx_score = round((purpose_score + seat_score + crowding_score) / 3, 4)

    return {
        "purpose_score": purpose_score,
        "seat_score": seat_score,
        "crowding_score": crowding_score,
        "ctx_score": ctx_score,
    }


def compute_final_ctx(location: str, purpose: str, seat: str, timestamp: str) -> float:
    base = compute_ctx_score(location, purpose, seat)
    slot = get_time_slot(timestamp)
    avail = AVAILABILITY.get(location, {}).get(slot, 0.0)
    return round(base * avail, 4)
