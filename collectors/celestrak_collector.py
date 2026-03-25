import httpx
from pipeline.tle_parser import parse_tle_file

# Space stations TLE feed (includes ISS)
STATIONS_URL = "https://celestrak.org/pub/TLE/stations.txt"


async def fetch_tle_catalog(url: str = STATIONS_URL) -> list[dict]:
    async with httpx.AsyncClient() as client:
        response = await client.get(url, timeout=10.0)
        response.raise_for_status()
    return parse_tle_file(response.text)


async def sync_tle_catalog():
    """Fetch latest TLEs and write to InfluxDB."""
    from storage.influx_writer import write_tle_record
    records = await fetch_tle_catalog()
    for record in records:
        write_tle_record(record)
    print(f"[TLE] Synced {len(records)} records.")

