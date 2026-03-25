from datetime import datetime, timezone
from sgp4.earth_gravity import wgs84
from sgp4.io import twoline2rv
import math


def propagate(tle_line1: str, tle_line2: str, dt: datetime = None) -> dict:
    """
    Propagate a TLE to a given datetime (default: now).
    Returns lat, lon, altitude in km, and velocity in km/s.
    """
    if dt is None:
        dt = datetime.now(timezone.utc)

    satellite = twoline2rv(tle_line1, tle_line2, wgs84)
    position, velocity = satellite.propagate(
        dt.year, dt.month, dt.day,
        dt.hour, dt.minute, dt.second + dt.microsecond / 1e6
    )

    if position is None:
        raise ValueError("SGP4 propagation failed — TLE may be expired.")

    lat, lon, alt = eci_to_geodetic(position, dt)
    speed = math.sqrt(sum(v ** 2 for v in velocity))  # km/s

    return {
        "latitude": lat,
        "longitude": lon,
        "altitude_km": alt,
        "velocity_km_s": speed,
        "timestamp": dt,
    }

def eci_to_geodetic(position: tuple, dt: datetime) -> tuple[float, float, float]:
    """Approximate ECI → geodetic conversion using Greenwich Sidereal Time."""
    x, y, z = position
    r = math.sqrt(x**2 + y**2 + z**2)

    jd = (dt - datetime(2000, 1, 1, 12, tzinfo=timezone.utc)).total_seconds() / 86400 + 2451545.0
    gst = (280.46061837 + 360.98564736629 * (jd - 2451545.0)) % 360

    lon = math.degrees(math.atan2(y, x)) - gst
    lon = (lon + 180) % 360 - 180
    lat = math.degrees(math.asin(z / r))
    alt = r - 6371.0  # subtract Earth's mean radius (km)

    return lat, lon, alt
    
    