from __future__ import annotations
from enum import Enum

from pydantic import BaseModel


class Purpose(str, Enum):
    FOCUS  = "FOCUS"   # 집중공부
    TEAM   = "TEAM"    # 팀플·그룹작업
    CASUAL = "CASUAL"  # 가볍게


class Seat(str, Enum):
    SOLO  = "SOLO"   # 혼자 앉을 자리
    GROUP = "GROUP"  # 여럿이 앉을 자리
    ANY   = "ANY"    # 상관없음


class Crowding(str, Enum):
    QUIET   = "QUIET"    # 한적한 곳 우선
    ANY     = "ANY"      # 상관없음
    LOUD_OK = "LOUD_OK"  # 혼잡해도 괜찮


class RecommendRequest(BaseModel):
    lat:       float
    lng:       float
    timestamp: str              # ISO 8601, +09:00 오프셋 포함
    top_n:     int      = 3
    purpose:   Purpose  = Purpose.FOCUS
    seat:      Seat     = Seat.ANY
    crowding:  Crowding = Crowding.ANY


class FeedbackRequest(BaseModel):
    location:   str
    rating:     int         # 1~5; 내부에서 (rating - 3) / 2 로 변환
    timestamp:  str         # ISO 8601, +09:00 오프셋 포함
    session_id: str | None = None
