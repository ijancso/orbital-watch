from fastapi import APIRouter, Query
from influxdb_client import InfluxDBClient
import config

router = APIRouter()


def _get_client():
    return InfluxDBClient(
        url=config.INFLUXDB_URL,
        token=config.INFLUXDB_TOKEN,
        org=config.INFLUXDB_ORG,
    )


@router.get("/")
def list_alerts(hours: int = Query(default=24, ge=1, le=168)):
    """Return all anomaly alerts logged in the last N hours."""
    client = _get_client()
    query = f"""
        from(bucket: "{config.INFLUXDB_BUCKET}")
          |> range(start: -{hours}h)
          |> filter(fn: (r) => r._measurement == "anomaly_alert")
          |> pivot(rowKey: ["_time"], columnKey: ["_field"], valueColumn: "_value")
    """
    tables = client.query_api().query(query)
    alerts = []
    for table in tables:
        for record in table.records:
            alerts.append({
                "timestamp": record["_time"],
                "norad_id": record.values.get("norad_id"),
                "satellite_name": record.values.get("satellite_name"),
                "alert_type": record.values.get("alert_type"),
                "severity": record.values.get("severity"),
                "message": record.get_value(),
            })
    return alerts


@router.get("/critical")
def list_critical_alerts(hours: int = Query(default=24, ge=1, le=168)):
    """Return only critical severity alerts from the last N hours."""
    client = _get_client()
    query = f"""
        from(bucket: "{config.INFLUXDB_BUCKET}")
          |> range(start: -{hours}h)
          |> filter(fn: (r) => r._measurement == "anomaly_alert")
          |> filter(fn: (r) => r.severity == "critical")
          |> pivot(rowKey: ["_time"], columnKey: ["_field"], valueColumn: "_value")
    """
    tables = client.query_api().query(query)
    alerts = []
    for table in tables:
        for record in table.records:
            alerts.append({
                "timestamp": record["_time"],
                "norad_id": record.values.get("norad_id"),
                "satellite_name": record.values.get("satellite_name"),
                "alert_type": record.values.get("alert_type"),
                "severity": record.values.get("severity"),
                "message": record.get_value(),
            })
    return alerts
