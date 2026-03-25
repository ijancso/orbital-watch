import httpx
import asyncio
from datetime import datetime, timezone
from storage.influx_writer import write_iss_position

ISS_API_URL = "http://api.open-notify.org/iss-now.json"
POLL_INTERVAL_SECONDS = 10


async def fetch_iss_position() -> dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(ISS_API_URL, timeout=5.0)
        response.raise_for_status()
        data = response.json()
    return {
        "timestamp": datetime.fromtimestamp(data["timestamp"], tz=timezone.utc),
        "latitude": float(data["iss_position"]["latitude"]),
        "longitude": float(data["iss_position"]["longitude"]),
    }


async def collect_loop():
    """Continuous polling loop — runs as a background scheduler job."""
    while True:
        try:
            position = await fetch_iss_position()
            write_iss_position(
                latitude=position["latitude"],
                longitude=position["longitude"],
                timestamp=position["timestamp"],
            )
            print(f"[{position['timestamp']}] ISS @ {position['latitude']:.4f}, {position['longitude']:.4f}")
        except Exception as e:
            print(f"[ERROR] ISS collector: {e}")
        await asyncio.sleep(POLL_INTERVAL_SECONDS)
