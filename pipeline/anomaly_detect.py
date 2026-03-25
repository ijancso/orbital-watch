from dataclasses import dataclass
from typing import Optional


@dataclass
class AnomalyAlert:
    satellite_name: str
    norad_id: int
    alert_type: str
    message: str
    severity: str  # "warning" | "critical"


def check_altitude_decay(
    norad_id: int,
    name: str,
    current_alt_km: float,
    previous_alt_km: float,
    threshold_km_per_day: float = 2.0,
) -> Optional[AnomalyAlert]:
    """Flag rapid altitude decay — may indicate reentry risk."""
    decay = previous_alt_km - current_alt_km
    if decay > threshold_km_per_day:
        severity = "critical" if decay > 5.0 else "warning"
        return AnomalyAlert(
            satellite_name=name,
            norad_id=norad_id,
            alert_type="ALTITUDE_DECAY",
            message=f"Altitude dropped {decay:.2f} km/day (threshold: {threshold_km_per_day})",
            severity=severity,
        )
    return None


def check_data_gap(
    norad_id: int,
    name: str,
    last_seen_seconds_ago: float,
    max_gap_seconds: float = 60.0,
) -> Optional[AnomalyAlert]:
    """Flag missing telemetry updates."""
    if last_seen_seconds_ago > max_gap_seconds:
        return AnomalyAlert(
            satellite_name=name,
            norad_id=norad_id,
            alert_type="DATA_GAP",
            message=f"No data for {last_seen_seconds_ago:.0f}s (max: {max_gap_seconds}s)",
            severity="warning",
        )
    return None
