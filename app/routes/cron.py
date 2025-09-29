import anyio
import time

from typing import Annotated
from fastapi import APIRouter, Depends

from ..cron import scheduler

router = APIRouter()


def job():
    print(f"定时任务执行: {time.strftime('%Y-%m-%d %H:%M:%S')}")

@router.get('/register_sechdule/{second}')
async def about():
    scheduler.add_job(job, "interval", seconds=3)  # 每 10 秒执行一次
