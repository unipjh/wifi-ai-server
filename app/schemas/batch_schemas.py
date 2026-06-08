from pydantic import BaseModel

from app.schemas.wifi_input import WifiMeasurement
from app.schemas.degradation_output import DegradationResult


class BatchComputeRequest(BaseModel):
    measurements: list[WifiMeasurement]  # 시간순 정렬, 동일 장소 또는 다중 장소 모두 가능


class BatchComputeResponse(BaseModel):
    results: list[DegradationResult]  # 입력 measurements와 동일 순서로 반환
