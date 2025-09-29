import anyio
import time

from fastapi import Depends, HTTPException, Security
from typing import Annotated
from fastapi import APIRouter, Depends

from ..cron import get_scheduler
from ..auth import api_key_header
router = APIRouter()


def job():
    print(f"定时任务执行: {time.strftime('%Y-%m-%d %H:%M:%S')}", flush=True)

@router.get('/register_scheduler/{second}')
async def about(second: int, _: str = Security(api_key_header)):

    get_scheduler().add_job(job, "interval", seconds=second)  # 每 10 秒执行一次

    return f'定时任务添加成功'