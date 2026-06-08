from fastapi import APIRouter

from app.schemas.wifi_input import WifiMeasurement
from app.schemas.degradation_output import DegradationResult
from app.schemas.batch_schemas import BatchComputeRequest, BatchComputeResponse
from app.services.degradation.scorer import compute_deg_score, batch_compute_deg_scores

router = APIRouter(prefix="/degradation", tags=["degradation"])


@router.post("/compute", response_model=DegradationResult)
def compute(measurement: WifiMeasurement) -> DegradationResult:
    return compute_deg_score(measurement)


@router.post("/batch_compute", response_model=BatchComputeResponse)
def batch_compute(request: BatchComputeRequest) -> BatchComputeResponse:
    results = batch_compute_deg_scores(request.measurements)
    return BatchComputeResponse(results=results)
