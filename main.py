from threading import Thread

from app import app
import anyio
import threading
import asyncio
import uvicorn
from fastapi import Security

async def run_server(app_str, port):
    config = uvicorn.Config(app_str, host="0.0.0.0", port=port, reload=False)
    server = uvicorn.Server(config)
    await server.serve()

async def main():
    async with anyio.create_task_group() as tg:
        tg.start_soon(run_server, 'app.app:app',8000)
        tg.start_soon(run_server, 'app.app:admin', 9000)

if __name__ == "__main__":
    anyio.run(main)

    # uvicorn.run("app.app:app", host="0.0.0.0", port=8000, reload=True)
