from fastapi import APIRouter

from app.schemas.recommendation_input import FeedbackRequest, RecommendRequest
from app.schemas.recommendation_output import RecommendResponse
from app.services.recommendation.recommender import process_feedback, recommend

router = APIRouter(prefix="/recommendation", tags=["recommendation"])


@router.post("/recommend", response_model=RecommendResponse)
def recommend_places(request: RecommendRequest) -> RecommendResponse:
    return recommend(request)


@router.post("/feedback")
def feedback(request: FeedbackRequest) -> dict[str, str]:
    process_feedback(request)
    return {"status": "ok"}
