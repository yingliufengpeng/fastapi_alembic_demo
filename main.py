from threading import Thread

from app import app
import anyio
import threading
import asyncio
import uvicorn

async def run_server(port):
    config = uvicorn.Config("app.app:app", host="0.0.0.0", port=port, reload=False)
    server = uvicorn.Server(config)
    await server.serve()

async def main():
    async with anyio.create_task_group() as tg:
        tg.start_soon(run_server, 8000)
        tg.start_soon(run_server, 9000)

if __name__ == "__main__":
    anyio.run(main)

    # uvicorn.run("app.app:app", host="0.0.0.0", port=8000, reload=True)
