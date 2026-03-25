from fastapi import FastAPI
from api.routes import iss, satellites, alerts

app = FastAPI(
    title="orbital-watch",
    description="Real-time spacecraft telemetry pipeline",
    version="0.1.0",
)

app.include_router(iss.router, prefix="/iss", tags=["ISS"])
app.include_router(satellites.router, prefix="/satellites", tags=["Satellites"])
app.include_router(alerts.router, prefix="/alerts", tags=["Alerts"])
