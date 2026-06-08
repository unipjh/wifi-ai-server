from pydantic import BaseModel


class PlaceScore(BaseModel):
    location:  str
    rec_score: float  # ∈ [0, 1]
    deg_score: float  # cached from Layer 1
    level:     str    # "Good" | "Fair" | "Poor"
    dist_norm: float  # normalised distance
    ctx_score: float  # compute_final_ctx() 반환값


    purpose_score:  float
    seat_score:     float
    crowding_score: float


class RecommendResponse(BaseModel):
    session_id: str           # UUID, 앱이 피드백 시 로컬 저장용
    places:     list[PlaceScore]
