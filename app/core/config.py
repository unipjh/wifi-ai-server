# EMA / EWMV smoothing coefficient — recommended range 0.1~0.3
ALPHA: float = 0.2

# Adaptive weight strength — recommended range 0.1~0.2
# Named LAMBDA_ to avoid shadowing Python built-in 'lambda'
LAMBDA_: float = 0.15

# RSSI normalization range (dBm) — 데이터 분석 후 조정
RSSI_BEST: float = -30.0   # dBm — 최상 신호 (0 degradation)
RSSI_WORST: float = -90.0  # dBm — 최악 신호 (1 degradation)

# Initial weights before real-data tuning (uniform 1/9 each)
# 키 이름은 API 필드명과 동일
INITIAL_WEIGHTS: dict[str, float] = {
    k: 1 / 9
    for k in (
        "rssi",
        "ping_gw", "jitter_gw", "packet_loss_gw",
        "ping_ext", "jitter_ext", "packet_loss_ext",
        "download_mbps", "upload_mbps",
    )
}

# Normalization ceilings: raw value / ceiling → [0, 1]
# Keys match CSV field names; values are 데이터 분석 후 조정 대상
NORM_MAX: dict[str, float] = {
    "ping_gw":          500.0,  # ms
    "jitter_gw":        200.0,  # ms
    "packet_loss_gw":   100.0,  # %
    "ping_ext":         500.0,  # ms
    "jitter_ext":       200.0,  # ms  — 데이터 분석 후 조정
    "packet_loss_ext":  100.0,  # %
    "download_mbps":    300.0,  # Mbps — 캠퍼스 Wi-Fi 상한
    "upload_mbps":      100.0,  # Mbps
}

# deg_score 레벨 임계값 — 데이터 분석 후 조정
# deg_score < DEG_GOOD_THRESHOLD  → "Good"
# deg_score < DEG_POOR_THRESHOLD  → "Fair"
# deg_score >= DEG_POOR_THRESHOLD → "Poor"
DEG_GOOD_THRESHOLD: float = 0.35
DEG_POOR_THRESHOLD: float = 0.65

# ── Layer 2 — Recommendation ──────────────────────────────────────────────────

DIST_MAX_M: float = 1000.0     # distance normalisation ceiling (metres)

# 수직 이동 비용 환산 계수: floor_m × FLOOR_COST_MULTIPLIER 만큼 수평 거리에 가산
# 엘리베이터 대기·이동 시간, 계단 체력 등 수평 대비 실질 비용이 높은 점을 반영
FLOOR_COST_MULTIPLIER: float = 4.0

# rec_score = α*(1-deg) + β*(1-dist) + γ*ctx,  α+β+γ=1
BETA: float = 0.25             # 거리 가중치 고정
POLICY_BLEND: float = 0.25     # fixed crowding weights 75% + learned policy 25%

CROWDING_ALPHA: dict[str, float] = {
    "QUIET":   0.55,
    "ANY":     0.35,
    "LOUD_OK": 0.15,
}

PURPOSE_WEIGHTS: dict[str, dict[str, float]] = {
    "FOCUS":  {"purpose": 0.5, "seat": 0.5},
    "TEAM":   {"purpose": 0.5, "seat": 0.5},
    "CASUAL": {"purpose": 0.7, "seat": 0.3},
}

CONTEXT_CROWDING_SHARE: float = 0.25

SEAT_KEY: dict[str, str | None] = {
    "SOLO":  "solo",
    "GROUP": "team",
    "ANY":   None,   # solo + team 평균
}

# ── Section 10-3: 사전 수집 데이터 기반 초기 정규화 파라미터 ──────────────────────
# 실측 후 채워넣을 것. 서버 첫 기동 후 1 윈도우(65분) 동안 EWMV 분포가 없으므로 사용.
_DEFAULT_STAT = lambda: {
    "rssi":            {"mean": -65.0, "std": 8.0},
    "ping_gw":         {"mean":   5.0, "std": 2.0},
    "jitter_gw":       {"mean":   2.0, "std": 1.0},
    "packet_loss_gw":  {"mean":   0.0, "std": 0.2},
    "ping_ext":        {"mean":  40.0, "std": 15.0},
    "jitter_ext":      {"mean":   5.0, "std": 3.0},
    "packet_loss_ext": {"mean":   0.0, "std": 0.5},
    "download_mbps":   {"mean":  50.0, "std": 20.0},
    "upload_mbps":     {"mean":  20.0, "std": 10.0},
}

INITIAL_STATS: dict = {loc: _DEFAULT_STAT() for loc in (
    "학술정보원_4층_열람실", "학생회관_5층_동아리방", "광개토관_15층_카페",
    "AI센터_1층_카페",       "AI센터_4층_과방",       "광개토관_B1_카페",
    "광개토관_7층_라운지",   "학술정보원_2층_라운지&카페",
    "학생회관_2층_카페",     "충무관_1층_카페",
)}

# ── Bandit ────────────────────────────────────────────────────────────────────

REC_INITIAL_WEIGHTS: dict[str, float] = {
    "deg": 0.40,
    "dist": 0.25,
    "purpose": 0.15,
    "seat": 0.10,
    "crowding": 0.10,
}
ETA: float = 0.05
EPSILON_INIT: float = 0.25
EPSILON_MIN: float = 0.05
EPSILON_DECAY_FACTOR: float = 0.95
EPSILON_DECAY_INTERVAL: int = 20

# Demo 서버용 인메모리 session 관리. 영속 저장소는 쓰지 않는다.
SESSION_TTL_SECONDS: int = 60 * 60
SESSION_MAX_SIZE: int = 1000
