import time

from contextlib import asynccontextmanager
from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = None


def get_scheduler():
    return scheduler

@asynccontextmanager
async def cron_life_span(app: FastAPI):
    # Startup 逻辑
    global scheduler
    print("cron_life_span startup", flush=True)
    scheduler = BackgroundScheduler()
    scheduler.start()
    yield
    # Shutdown 逻辑
    scheduler.shutdown()
    print("cron_life_span shutdown", flush=True)





