from fastapi import APIRouter, HTTPException
from pipeline.tle_parser import parse_tle_file
from pipeline.orbit_calc import propagate
from storage.influx_writer import get_write_api
import config
import httpx

router = APIRouter()

STATIONS_URL = "https://celestrak.org/pub/TLE/stations.txt"


@router.get("/")
async def list_satellites():
    """Return a list of all tracked satellites from the latest Celestrak feed."""
    async with httpx.AsyncClient() as client:
        response = await client.get(STATIONS_URL, timeout=10.0)
        response.raise_for_status()
    records = parse_tle_file(response.text)
    return [{"norad_id": r["norad_id"], "name": r["name"]} for r in records]


@router.get("/{norad_id}/tle")
async def get_tle(norad_id: int):
    """Return the latest TLE for a given NORAD ID."""
    async with httpx.AsyncClient() as client:
        response = await client.get(STATIONS_URL, timeout=10.0)
        response.raise_for_status()
    records = parse_tle_file(response.text)
    match = next((r for r in records if r["norad_id"] == norad_id), None)
    if not match:
        raise HTTPException(status_code=404, detail=f"No TLE found for NORAD ID {norad_id}")
    return match


@router.get("/{norad_id}/position")
async def get_position(norad_id: int):
    """Propagate the current position of a satellite from its latest TLE."""
    async with httpx.AsyncClient() as client:
        response = await client.get(STATIONS_URL, timeout=10.0)
        response.raise_for_status()
    records = parse_tle_file(response.text)
    match = next((r for r in records if r["norad_id"] == norad_id), None)
    if not match:
        raise HTTPException(status_code=404, detail=f"No TLE found for NORAD ID {norad_id}")
    result = propagate(match["tle_line1"], match["tle_line2"])
    result["name"] = match["name"]
    result["norad_id"] = norad_id
    return result
