from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from datetime import datetime
import config

_client = None
_write_api = None


def get_write_api():
    global _client, _write_api
    if _write_api is None:
        _client = InfluxDBClient(
            url=config.INFLUXDB_URL,
            token=config.INFLUXDB_TOKEN,
            org=config.INFLUXDB_ORG,
        )
        _write_api = _client.write_api(write_options=SYNCHRONOUS)
    return _write_api


def write_iss_position(latitude: float, longitude: float, timestamp: datetime):
    point = (
        Point("iss_position")
        .field("latitude", latitude)
        .field("longitude", longitude)
        .time(timestamp, WritePrecision.SECONDS)
    )
    get_write_api().write(bucket=config.INFLUXDB_BUCKET, record=point)


def write_orbital_state(
    norad_id: int,
    name: str,
    latitude: float,
    longitude: float,
    altitude_km: float,
    velocity_km_s: float,
    timestamp: datetime,
):
    point = (
        Point("orbital_state")
        .tag("norad_id", str(norad_id))
        .tag("satellite_name", name)
        .field("latitude", latitude)
        .field("longitude", longitude)
        .field("altitude_km", altitude_km)
        .field("velocity_km_s", velocity_km_s)
        .time(timestamp, WritePrecision.SECONDS)
    )
    get_write_api().write(bucket=config.INFLUXDB_BUCKET, record=point)


def write_tle_record(record: dict):
    point = (
        Point("tle_record")
        .tag("norad_id", str(record["norad_id"]))
        .tag("satellite_name", record["name"])
        .field("tle_line1", record["tle_line1"])
        .field("tle_line2", record["tle_line2"])
        .time(record["epoch"], WritePrecision.SECONDS)
    )
    get_write_api().write(bucket=config.INFLUXDB_BUCKET, record=point)


def write_anomaly(
    norad_id: int,
    satellite_name: str,
    alert_type: str,
    severity: str,
    message: str,
    timestamp: datetime,
):
    point = (
        Point("anomaly_alert")
        .tag("norad_id", str(norad_id))
        .tag("satellite_name", satellite_name)
        .tag("alert_type", alert_type)
        .tag("severity", severity)
        .field("message", message)
        .time(timestamp, WritePrecision.SECONDS)
    )
    get_write_api().write(bucket=config.INFLUXDB_BUCKET, record=point)

