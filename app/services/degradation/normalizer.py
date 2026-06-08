from app.core.config import NORM_MAX, RSSI_BEST, RSSI_WORST
from app.schemas.wifi_input import WifiMeasurement

def normalize(measurement: WifiMeasurement) -> dict[str, float]:
    """
    Raw IoT measurements → [0, 1] normalized values.

    rssi and throughput are inverted: higher raw value = lower degradation.
    download/upload absent (None) → those keys are omitted from the returned
    dict so update_ewmv carries forward their EWMVState.mu unchanged.
    """
    rssi_range = RSSI_BEST - RSSI_WORST  # 60.0 dBm
    rssi_norm = 1.0 - min(max((measurement.rssi - RSSI_WORST) / rssi_range, 0.0), 1.0)

    norm: dict[str, float] = {
        "rssi":            rssi_norm,
        "ping_gw":         min(measurement.ping_gw  / NORM_MAX["ping_gw"],  1.0),
        "jitter_gw":       min(measurement.jitter_gw / NORM_MAX["jitter_gw"], 1.0),
        "packet_loss_gw":  min(measurement.packet_loss_gw / NORM_MAX["packet_loss_gw"], 1.0),
        "ping_ext":        min(measurement.ping_ext / NORM_MAX["ping_ext"], 1.0),
        "jitter_ext":      min(measurement.jitter_ext / NORM_MAX["jitter_ext"], 1.0),
        "packet_loss_ext": min(measurement.packet_loss_ext / NORM_MAX["packet_loss_ext"], 1.0),
    }

    if measurement.download_mbps is not None:
        norm["download_mbps"] = 1.0 - min(measurement.download_mbps / NORM_MAX["download_mbps"], 1.0)

    if measurement.upload_mbps is not None:
        norm["upload_mbps"] = 1.0 - min(measurement.upload_mbps / NORM_MAX["upload_mbps"], 1.0)

    return norm
