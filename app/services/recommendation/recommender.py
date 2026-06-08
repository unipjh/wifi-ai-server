from app.core.config import DEG_GOOD_THRESHOLD, DEG_POOR_THRESHOLD
from app.schemas.recommendation_input import FeedbackRequest, RecommendRequest
from app.schemas.recommendation_output import PlaceScore, RecommendResponse
from app.services.degradation.scorer import get_latest_deg_score
from app.services.recommendation import bandit, policy
from app.services.recommendation.ctx_store import compute_context_features
from app.services.recommendation.rec_scorer import compute_dist_norm, compute_rec_score
from app.services.recommendation.session_store import create_session, get_session_place, record_feedback
from app.services.recommendation.venue_profiles import VENUE_PROFILE


def _deg_level(score: float) -> str:
    if score < DEG_GOOD_THRESHOLD:
        return "Good"
    if score < DEG_POOR_THRESHOLD:
        return "Fair"
    return "Poor"


def recommend(request: RecommendRequest) -> RecommendResponse:
    crowding = request.crowding.value
    purpose = request.purpose.value
    seat = request.seat.value
    learned_weights = policy.get_weights()

    results: list[PlaceScore] = []
    for location, profile in VENUE_PROFILE.items():
        context = compute_context_features(location, purpose, seat, crowding, request.timestamp)
        ctx = context["ctx_score"]

        if ctx == 0.0:
            continue

        deg  = get_latest_deg_score(location)
        dist = compute_dist_norm(request.lat, request.lng, profile["lat"], profile["lng"], profile["floor_m"])
        rec  = compute_rec_score(
            deg,
            dist,
            context["purpose_score"],
            context["seat_score"],
            context["crowding_score"],
            crowding,
            purpose,
            learned_weights,
        )

        results.append(PlaceScore(
            location=location,
            rec_score=rec,
            deg_score=round(deg, 4),
            level=_deg_level(deg),
            dist_norm=dist,
            ctx_score=ctx,
            purpose_score=context["purpose_score"],
            seat_score=context["seat_score"],
            crowding_score=context["crowding_score"],
        ))

    selected, _ = bandit.select_zones(results, request.top_n)
    sid = create_session(
        purpose, seat,
        crowding, request.top_n, selected, request.timestamp,
    )
    return RecommendResponse(session_id=sid, places=selected)


def process_feedback(request: FeedbackRequest) -> None:
    reward = (request.rating - 3) / 2   # -1.0 ~ 1.0

    session_place = None
    if request.session_id:
        session_place = get_session_place(request.session_id, request.location)
        record_feedback(request.session_id, request.location, request.rating, request.timestamp)

    if session_place is not None:
        deg = session_place["deg_score"]
        dist = session_place["dist_norm"]
        purpose_score = session_place["purpose_score"]
        seat_score = session_place["seat_score"]
        crowding_score = session_place["crowding_score"]
    else:
        deg = get_latest_deg_score(request.location)
        # session_id 없는 기존 호출은 목적/좌석/거리 정보를 중립값으로 근사한다.
        context = compute_context_features(request.location, "FOCUS", "ANY", "ANY", request.timestamp)
        purpose_score = context["purpose_score"]
        seat_score = context["seat_score"]
        crowding_score = context["crowding_score"]
        dist = 0.5

    policy.update_policy(reward, deg, dist, purpose_score, seat_score, crowding_score)
    bandit.record_feedback_and_decay()
