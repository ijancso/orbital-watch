import os
from dotenv import load_dotenv

load_dotenv()

INFLUXDB_URL = os.getenv("INFLUXDB_URL", "http://localhost:8086")
INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN", "")
INFLUXDB_ORG = os.getenv("INFLUXDB_ORG", "orbital-watch")
INFLUXDB_BUCKET = os.getenv("INFLUXDB_BUCKET", "telemetry")

SPACETRACK_USERNAME = os.getenv("SPACETRACK_USERNAME", "")
SPACETRACK_PASSWORD = os.getenv("SPACETRACK_PASSWORD", "")

ISS_POLL_INTERVAL = int(os.getenv("ISS_POLL_INTERVAL", "10"))       # seconds
TLE_SYNC_INTERVAL_HOURS = int(os.getenv("TLE_SYNC_INTERVAL_HOURS", "6"))
