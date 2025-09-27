from typing import Annotated
from fastapi import APIRouter, Depends
import anyio
router = APIRouter()


@router.get('/about')
async def about():
    print(f'about is processing ...')
    task = anyio.get_current_task()
    print(f"Current task: {task!r}")
    print(f"Task name: {task.name}")
    return 'v1'