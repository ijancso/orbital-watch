from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from collectors.iss_collector import collect_loop
from collectors.celestrak_collector import sync_tle_catalog
import asyncio

scheduler = AsyncIOScheduler()


def setup_jobs():
    # Sync TLE catalog every 6 hours
    scheduler.add_job(
        lambda: asyncio.create_task(sync_tle_catalog()),
        IntervalTrigger(hours=6),
        id="tle_sync",
        replace_existing=True,
    )


if __name__ == "__main__":
    setup_jobs()
    scheduler.start()
    print("Scheduler started. Running ISS collector...")
    asyncio.run(collect_loop())
