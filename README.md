<!-- problem-first-summary:start -->
**Huge Problem(Pain Point):** RSSI·지연·손실률 같은 원시 WiFi 지표만으로는 품질 저하와 다음 측정 장소를 일관되게 판단하기 어렵다.

**솔루션 한 줄 정의:** 품질 저하 점수와 피드백 기반 측정 장소 추천을 FastAPI 엔드포인트로 제공한다.

**현재 상태:** WiFi 시스템 API

**문제 해결 중심의 사고 흐름**

1. **관찰** — 현장 측정값이 많아져도 각 지표를 사람이 따로 해석하면 판단 기준과 다음 수집 위치가 달라졌다.
2. **선택** — 저하 점수 계산과 추천·피드백을 별도 서비스 경계로 분리했다.
3. **구현** — FastAPI의 `/degradation/compute`, batch compute, `/recommendation/recommend`, feedback API와 서비스 계층을 구성했다.
4. **검증과 한계** — 코드와 엔드포인트는 존재하지만 README와 공개 실행 예시가 없어 현재 재현성은 제한적이다.
<!-- problem-first-summary:end -->

---
# Wi-Fi Recommendation AI Server

A FastAPI service that converts raw Wi-Fi measurements into a degradation score and recommends measurement or study locations using context and feedback.

## API surface

- POST /api/v1/degradation/compute: score one Wi-Fi measurement.
- POST /api/v1/degradation/batch_compute: score multiple measurements.
- POST /api/v1/recommendation/recommend: return ranked places for purpose, seating, crowding, location, and time context.
- POST /api/v1/recommendation/feedback: update recommendation context from a 1-5 rating.

Degradation results use a 0-1 score where 0 is best and 1 is worst, together with Good, Fair, or Poor levels.

## Data flow

1. The collector sends RSSI, gateway and external latency, jitter, packet loss, and optional throughput.
2. The degradation service normalizes the metrics and computes a quality score.
3. The recommendation service combines cached quality, distance, purpose, seating, crowding, and feedback context.
4. The client stores the returned session ID and sends it with later feedback when available.

## Run locally

1. Install packages with pip install -r requirements.txt.
2. Start the API with uvicorn main:app --reload.
3. Open /docs for the generated OpenAPI interface.

## Current limits

The repository currently has no automated test suite or persisted production feedback store documented. API behavior should be validated with representative campus measurements before operational use.
