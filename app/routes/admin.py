from typing import Annotated
from fastapi import APIRouter, Depends
import anyio
router = APIRouter()


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