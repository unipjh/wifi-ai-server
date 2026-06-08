from __future__ import annotations
import time
import uuid

from app.core.config import SESSION_MAX_SIZE, SESSION_TTL_SECONDS

SESSION_STORE: dict[str, dict] = {}


def _cleanup_expired(now: float | None = None) -> None:
    now = time.time() if now is None else now
    expired = [
        sid for sid, data in SESSION_STORE.items()
        if now - data.get("created_at", now) > SESSION_TTL_SECONDS
    ]
    for sid in expired:
        SESSION_STORE.pop(sid, None)

    overflow = len(SESSION_STORE) - SESSION_MAX_SIZE
    if overflow <= 0:
        return

    oldest = sorted(
        SESSION_STORE,
        key=lambda sid: SESSION_STORE[sid].get("created_at", 0.0),
    )
    for sid in oldest[:overflow]:
        SESSION_STORE.pop(sid, None)


def create_session(
    purpose:   str,
    seat:      str,
    crowding:  str,
    top_n:     int,
    results:   list,
    timestamp: str,
) -> str:
    _cleanup_expired()
    sid = str(uuid.uuid4())
    SESSION_STORE[sid] = {
        "created_at": time.time(),
        "timestamp": timestamp,
        "purpose":   purpose,
        "seat":      seat,
        "crowding":  crowding,
        "top_n":     top_n,
        "results":   [
            {
                "location":  p.location,
                "rec_score": p.rec_score,
                "deg_score": p.deg_score,
                "dist_norm": p.dist_norm,
                "ctx_score": p.ctx_score,
                "purpose_score": p.purpose_score,
                "seat_score": p.seat_score,
                "crowding_score": p.crowding_score,
                "level":     p.level,
            }
            for p in results
        ],
        "feedback":  None,
    }
    return sid


def get_session(session_id: str) -> dict | None:
    _cleanup_expired()
    return SESSION_STORE.get(session_id)


def get_session_place(session_id: str, location: str) -> dict | None:
    session = get_session(session_id)
    if session is None:
        return None
    for place in session["results"]:
        if place["location"] == location:
            return place
    return None


def record_feedback(session_id: str, location: str, rating: int, timestamp: str) -> None:
    session = get_session(session_id)
    if session is None:
        return
    session["feedback"] = {
        "location": location,
        "rating": rating,
        "timestamp": timestamp,
    }
