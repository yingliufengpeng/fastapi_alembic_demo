import anyio

from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi import FastAPI, BackgroundTasks

router = APIRouter()

# 定义一个异步生成器
async def steps(name: str):
    for i in range(5):
        await anyio.sleep(1)
        yield f"Task {name} step {i}"

# 使用 async for 消费
async def long_task(name: str):
    async for msg in steps(name):
        print(msg, flush=True)

@router.get("/start-task")
async def start_task(background_tasks: BackgroundTasks):
    background_tasks.add_task(long_task, "A")
    return {"status": "started"}


@router.get('/admin')
async def about():
    while True:
        # breakpoint()
        print("admin is processing ...", flush=True)
        task = anyio.get_current_task()
        print(f"Current task: {task!r}")
        print(f"Task name: {task.name}")
        await anyio.sleep(1)

    return 'admin'