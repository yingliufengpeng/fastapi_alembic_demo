import time

from contextlib import asynccontextmanager
from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = None

@asynccontextmanager
async def cron_life_span(app: FastAPI):
    # Startup 逻辑
    global scheduler
    print("Application startup", flush=True)
    scheduler = BackgroundScheduler()
    scheduler.add_job(job, "interval", seconds=10)  # 每 10 秒执行一次
    scheduler.start()
    yield
    # Shutdown 逻辑
    scheduler.shutdown()
    print("Application shutdown", flush=True)





