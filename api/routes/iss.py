from fastapi import APIRouter, Query
from collectors.iss_collector import fetch_iss_position

router = APIRouter()


@router.get("/position")
async def get_current_position():
    """Fetch live ISS position from Open Notify."""
    return await fetch_iss_position()


@router.get("/history")
def get_history(hours: int = Query(default=1, ge=1, le=72)):
    """Return stored ISS positions from the last N hours."""
    from influxdb_client import InfluxDBClient
    import config

    client = InfluxDBClient(
        url=config.INFLUXDB_URL,
        token=config.INFLUXDB_TOKEN,
        org=config.INFLUXDB_ORG,
    )
    query = f"""
        from(bucket: "{config.INFLUXDB_BUCKET}")
          |> range(start: -{hours}h)
          |> filter(fn: (r) => r._measurement == "iss_position")
          |> pivot(rowKey: ["_time"], columnKey: ["_field"], valueColumn: "_value")
    """
    tables = client.query_api().query(query)
    return [
        {"timestamp": record["_time"], "latitude": record["latitude"], "longitude": record["longitude"]}
        for table in tables
        for record in table.records
    ]
