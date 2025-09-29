import time
import anyio

from contextlib import asynccontextmanager
from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = None


def get_scheduler():
    return scheduler


async def process():
    print(f'running process ...', flush=True)

def wrapper():
    anyio.run(process)

@asynccontextmanager
async def life_span(app: FastAPI):
    # Startup 逻辑
    global scheduler
    print("cron_life_span startup", flush=True)
    scheduler = BackgroundScheduler()
    scheduler.start()
    # scheduler.add_job(wrapper, 'interval', seconds=3)
    # 添加任务：每周凌晨3点执行
    scheduler.add_job(
        wrapper,
        trigger='cron',
        day_of_week='mon',  # 可改为 '0' 或 'mon' 表示周一
        hour=3,
        minute=0,
        second=0,
        id='weekly_job'
    )
    yield
    # Shutdown 逻辑
    scheduler.shutdown()
    print("cron_life_span shutdown", flush=True)





