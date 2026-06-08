from pydantic import BaseModel


class WifiMeasurement(BaseModel):
    timestamp:        str            # ISO 8601, +09:00 오프셋 포함
    ssid:             str
    location:         str            # 건물명_층_공간명 형식 (예: 광개토관_15층_카페)
    rssi:             float          # dBm
    ping_gw:          float          # ms — 라우터 핑
    jitter_gw:        float          # ms — 라우터 구간 jitter
    packet_loss_gw:   float          # % — 라우터 구간 패킷 손실률
    ping_ext:         float          # ms — 인터넷 외부 핑
    jitter_ext:       float          # ms — 인터넷 구간 jitter
    packet_loss_ext:  float          # % — 인터넷 구간 패킷 손실률
    download_mbps:    float | None = None
    upload_mbps:      float | None = None
