import random

from app.core.config import (
    EPSILON_DECAY_FACTOR,
    EPSILON_DECAY_INTERVAL,
    EPSILON_INIT,
    EPSILON_MIN,
)
from app.schemas.recommendation_output import PlaceScore

_epsilon: float = EPSILON_INIT
_feedback_count: int = 0


def get_epsilon() -> float:
    return _epsilon


def select_zones(
    scored_places: list[PlaceScore],
    top_n: int,
) -> tuple[list[PlaceScore], bool]:
    n = min(top_n, len(scored_places))
    if random.random() < _epsilon:
        selected = random.sample(scored_places, n)
        return selected, True
    else:
        sorted_places = sorted(scored_places, key=lambda p: p.rec_score, reverse=True)
        return sorted_places[:n], False


def record_feedback_and_decay() -> None:
    global _epsilon, _feedback_count
    _feedback_count += 1
    if _feedback_count % EPSILON_DECAY_INTERVAL == 0:
        _epsilon = max(_epsilon * EPSILON_DECAY_FACTOR, EPSILON_MIN)
