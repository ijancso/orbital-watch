import asyncio
from apscheduler.schedulers.background import BackgroundScheduler
from collectors.iss_collector import collect_loop
from collectors.celestrak_collector import sync_tle_catalog

scheduler = BackgroundScheduler()


def run_sync_tle():
    """Wrapper to run async TLE sync from a background thread."""
    asyncio.run(sync_tle_catalog())


def setup_jobs():
    # Sync TLE catalog every 6 hours
    scheduler.add_job(
        run_sync_tle,
        "interval",
        hours=6,
        id="tle_sync",
        replace_existing=True,
    )


if __name__ == "__main__":
    setup_jobs()
    scheduler.start()
    print("Scheduler started. Running ISS collector...")
    # asyncio.run() creates and manages the event loop — AsyncIOScheduler not needed
    asyncio.run(collect_loop())
