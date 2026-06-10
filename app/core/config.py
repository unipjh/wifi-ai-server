"""Runtime configuration calibrated from ``collected_data``.

Calibration source:
- collected_data/main/*.csv and collected_data/sub/*.csv
- 21,736 measurements collected on 2026-06-08

Layer 1 values are intentionally robust rather than max-based. Latency,
jitter, and packet-loss ceilings use the observed p95 neighborhood so that
"clearly bad" measurements saturate instead of being diluted by rare spikes.
Throughput ceilings use observed p95 as the "good enough" point.
"""

# EMA / EWMV smoothing coefficient. With roughly 1-minute samples, 0.2 keeps
# the effective memory near the last 5 measurements.
ALPHA: float = 0.2

# Adaptive weight strength. Because INITIAL_WEIGHTS are now data-calibrated,
# keep online variance adaptation useful but secondary.
# Named LAMBDA_ to avoid shadowing Python built-in 'lambda'.
LAMBDA_: float = 0.15

# RSSI normalization range (dBm), based on robust observed campus range.
# RSSI >= RSSI_BEST is treated as 0 degradation; RSSI <= RSSI_WORST as 1.
RSSI_BEST: float = -42.0
RSSI_WORST: float = -75.0

# Initial degradation weights derived from normalized real-data badness:
# 0.45 * mean + 0.35 * p90 + 0.20 * std, then normalized to sum to 1.
INITIAL_WEIGHTS: dict[str, float] = {
    "rssi": 0.132,
    "ping_gw": 0.084,
    "jitter_gw": 0.086,
    "packet_loss_gw": 0.071,
    "ping_ext": 0.147,
    "jitter_ext": 0.082,
    "packet_loss_ext": 0.087,
    "download_mbps": 0.151,
    "upload_mbps": 0.160,
}

# Normalization ceilings. For throughput, higher is better and the normalizer
# inverts the value: degradation = 1 - min(raw / ceiling, 1).
NORM_MAX: dict[str, float] = {
    "ping_gw": 90.0,          # ms, near p95=84.27
    "jitter_gw": 60.0,        # ms, near p95=53.82
    "packet_loss_gw": 15.0,   # %, near p95=13.28
    "ping_ext": 110.0,        # ms, near p95=105.07
    "jitter_ext": 55.0,       # ms, near p95=52.34
    "packet_loss_ext": 30.0,  # %, near p95=28.19
    "download_mbps": 90.0,    # Mbps, observed p95=85.07
    "upload_mbps": 55.0,      # Mbps, observed p95=50.10
}

# Thresholds calibrated by replaying every CSV in collected_data with
# location-specific EWMV priors: p40 ~= 0.305, p90 ~= 0.501.
DEG_GOOD_THRESHOLD: float = 0.31
DEG_POOR_THRESHOLD: float = 0.50

# ----- Layer 2: Recommendation ------------------------------------------------

DIST_MAX_M: float = 1000.0

# Vertical travel cost. One floor is approximated as 4 meters of horizontal
# travel burden to account for elevator/wait/stair effort.
FLOOR_COST_MULTIPLIER: float = 4.0

# rec_score = alpha*(1-deg) + beta*(1-dist) + context terms.
BETA: float = 0.25
POLICY_BLEND: float = 0.25

CROWDING_ALPHA: dict[str, float] = {
    "QUIET": 0.55,
    "ANY": 0.35,
    "LOUD_OK": 0.15,
}

PURPOSE_WEIGHTS: dict[str, dict[str, float]] = {
    "FOCUS": {"purpose": 0.5, "seat": 0.5},
    "TEAM": {"purpose": 0.5, "seat": 0.5},
    "CASUAL": {"purpose": 0.7, "seat": 0.3},
}

CONTEXT_CROWDING_SHARE: float = 0.25

SEAT_KEY: dict[str, str | None] = {
    "SOLO": "solo",
    "GROUP": "team",
    "ANY": None,
}

# ----- Initial raw statistics from collected_data -----------------------------

_DEFAULT_STAT = lambda: {
    "rssi": {"mean": -56.08, "std": 7.85},
    "ping_gw": {"mean": 18.61, "std": 35.10},
    "jitter_gw": {"mean": 16.28, "std": 34.36},
    "packet_loss_gw": {"mean": 5.06, "std": 18.29},
    "ping_ext": {"mean": 58.08, "std": 28.29},
    "jitter_ext": {"mean": 12.39, "std": 25.28},
    "packet_loss_ext": {"mean": 6.70, "std": 18.43},
    "download_mbps": {"mean": 44.49, "std": 22.42},
    "upload_mbps": {"mean": 26.05, "std": 15.59},
}

INITIAL_STATS: dict[str, dict[str, dict[str, float]]] = {
    "AI센터_1층_카페": {
        "rssi": {"mean": -63.86, "std": 8.58},
        "ping_gw": {"mean": 24.17, "std": 46.01},
        "jitter_gw": {"mean": 28.11, "std": 62.56},
        "packet_loss_gw": {"mean": 1.58, "std": 7.21},
        "ping_ext": {"mean": 56.12, "std": 20.13},
        "jitter_ext": {"mean": 14.58, "std": 23.98},
        "packet_loss_ext": {"mean": 3.60, "std": 15.84},
        "download_mbps": {"mean": 27.82, "std": 16.56},
        "upload_mbps": {"mean": 23.23, "std": 15.31},
    },
    "AI센터_4층_과방": {
        "rssi": {"mean": -50.01, "std": 7.43},
        "ping_gw": {"mean": 6.03, "std": 4.48},
        "jitter_gw": {"mean": 6.01, "std": 6.73},
        "packet_loss_gw": {"mean": 12.20, "std": 32.14},
        "ping_ext": {"mean": 44.41, "std": 14.53},
        "jitter_ext": {"mean": 1.92, "std": 2.68},
        "packet_loss_ext": {"mean": 12.57, "std": 32.07},
        "download_mbps": {"mean": 49.79, "std": 32.92},
        "upload_mbps": {"mean": 24.04, "std": 31.75},
    },
    "광개토관_15층_카페": {
        "rssi": {"mean": -53.83, "std": 6.45},
        "ping_gw": {"mean": 19.72, "std": 31.25},
        "jitter_gw": {"mean": 12.07, "std": 26.45},
        "packet_loss_gw": {"mean": 5.71, "std": 18.72},
        "ping_ext": {"mean": 54.56, "std": 24.35},
        "jitter_ext": {"mean": 9.07, "std": 19.11},
        "packet_loss_ext": {"mean": 7.68, "std": 18.77},
        "download_mbps": {"mean": 42.45, "std": 10.45},
        "upload_mbps": {"mean": 31.05, "std": 12.14},
    },
    "광개토관_7층_라운지": {
        "rssi": {"mean": -53.71, "std": 7.16},
        "ping_gw": {"mean": 19.98, "std": 25.28},
        "jitter_gw": {"mean": 13.48, "std": 15.05},
        "packet_loss_gw": {"mean": 9.05, "std": 27.90},
        "ping_ext": {"mean": 61.31, "std": 37.50},
        "jitter_ext": {"mean": 11.78, "std": 18.07},
        "packet_loss_ext": {"mean": 9.70, "std": 27.88},
        "download_mbps": {"mean": 16.85, "std": 9.35},
        "upload_mbps": {"mean": 16.97, "std": 13.10},
    },
    "광개토관_B1_카페": {
        "rssi": {"mean": -64.24, "std": 5.02},
        "ping_gw": {"mean": 15.53, "std": 28.07},
        "jitter_gw": {"mean": 13.64, "std": 26.03},
        "packet_loss_gw": {"mean": 7.29, "std": 24.75},
        "ping_ext": {"mean": 50.60, "std": 18.10},
        "jitter_ext": {"mean": 9.90, "std": 14.83},
        "packet_loss_ext": {"mean": 7.44, "std": 24.63},
        "download_mbps": {"mean": 41.35, "std": 16.05},
        "upload_mbps": {"mean": 33.22, "std": 17.59},
    },
    "충무관_1층_카페": {
        "rssi": {"mean": -64.47, "std": 4.63},
        "ping_gw": {"mean": 23.47, "std": 47.10},
        "jitter_gw": {"mean": 22.27, "std": 40.34},
        "packet_loss_gw": {"mean": 3.27, "std": 14.37},
        "ping_ext": {"mean": 61.96, "std": 27.05},
        "jitter_ext": {"mean": 16.41, "std": 26.41},
        "packet_loss_ext": {"mean": 3.18, "std": 13.11},
        "download_mbps": {"mean": 29.07, "std": 16.50},
        "upload_mbps": {"mean": 14.59, "std": 11.73},
    },
    "학생회관_2층_카페": {
        "rssi": {"mean": -51.64, "std": 5.50},
        "ping_gw": {"mean": 54.76, "std": 82.84},
        "jitter_gw": {"mean": 58.09, "std": 83.71},
        "packet_loss_gw": {"mean": 10.46, "std": 28.04},
        "ping_ext": {"mean": 99.00, "std": 42.72},
        "jitter_ext": {"mean": 42.00, "std": 62.94},
        "packet_loss_ext": {"mean": 8.59, "std": 25.88},
        "download_mbps": {"mean": 17.61, "std": 7.37},
        "upload_mbps": {"mean": 12.12, "std": 7.85},
    },
    # No direct 5F club-room sample yet; use the same building's 2F cafe as
    # a conservative proxy until dedicated measurements are collected.
    "학생회관_5층_동아리방": {
        "rssi": {"mean": -51.64, "std": 5.50},
        "ping_gw": {"mean": 54.76, "std": 82.84},
        "jitter_gw": {"mean": 58.09, "std": 83.71},
        "packet_loss_gw": {"mean": 10.46, "std": 28.04},
        "ping_ext": {"mean": 99.00, "std": 42.72},
        "jitter_ext": {"mean": 42.00, "std": 62.94},
        "packet_loss_ext": {"mean": 8.59, "std": 25.88},
        "download_mbps": {"mean": 17.61, "std": 7.37},
        "upload_mbps": {"mean": 12.12, "std": 7.85},
    },
    "학술정보원_2층_라운지": {
        "rssi": {"mean": -59.55, "std": 6.76},
        "ping_gw": {"mean": 12.12, "std": 13.09},
        "jitter_gw": {"mean": 13.97, "std": 16.91},
        "packet_loss_gw": {"mean": 2.71, "std": 14.37},
        "ping_ext": {"mean": 55.17, "std": 19.97},
        "jitter_ext": {"mean": 11.56, "std": 21.22},
        "packet_loss_ext": {"mean": 1.97, "std": 7.50},
        "download_mbps": {"mean": 62.37, "std": 25.32},
        "upload_mbps": {"mean": 27.78, "std": 15.22},
    },
    "학술정보원_2층_라운지&카페": {
        "rssi": {"mean": -59.55, "std": 6.76},
        "ping_gw": {"mean": 12.12, "std": 13.09},
        "jitter_gw": {"mean": 13.97, "std": 16.91},
        "packet_loss_gw": {"mean": 2.71, "std": 14.37},
        "ping_ext": {"mean": 55.17, "std": 19.97},
        "jitter_ext": {"mean": 11.56, "std": 21.22},
        "packet_loss_ext": {"mean": 1.97, "std": 7.50},
        "download_mbps": {"mean": 62.37, "std": 25.32},
        "upload_mbps": {"mean": 27.78, "std": 15.22},
    },
    "학술정보원_3층": {
        "rssi": {"mean": -56.54, "std": 7.60},
        "ping_gw": {"mean": 12.21, "std": 20.74},
        "jitter_gw": {"mean": 14.08, "std": 20.18},
        "packet_loss_gw": {"mean": 2.14, "std": 6.44},
        "ping_ext": {"mean": 58.08, "std": 26.64},
        "jitter_ext": {"mean": 12.49, "std": 20.79},
        "packet_loss_ext": {"mean": 5.26, "std": 9.64},
        "download_mbps": {"mean": 58.82, "std": 23.47},
        "upload_mbps": {"mean": 24.80, "std": 13.40},
    },
    # No direct 4F reading-room sample yet; use the library 3F sample as the
    # closest same-building network proxy.
    "학술정보원_4층_열람실": {
        "rssi": {"mean": -56.54, "std": 7.60},
        "ping_gw": {"mean": 12.21, "std": 20.74},
        "jitter_gw": {"mean": 14.08, "std": 20.18},
        "packet_loss_gw": {"mean": 2.14, "std": 6.44},
        "ping_ext": {"mean": 58.08, "std": 26.64},
        "jitter_ext": {"mean": 12.49, "std": 20.79},
        "packet_loss_ext": {"mean": 5.26, "std": 9.64},
        "download_mbps": {"mean": 58.82, "std": 23.47},
        "upload_mbps": {"mean": 24.80, "std": 13.40},
    },
}

# ----- Bandit -----------------------------------------------------------------

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

# Demo server in-memory session storage. Data is not persisted.
SESSION_TTL_SECONDS: int = 60 * 60
SESSION_MAX_SIZE: int = 1000
