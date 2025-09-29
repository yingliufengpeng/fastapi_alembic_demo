import anyio
from client.web_stocket import connent_ws

async def main():
    async with anyio.create_task_group() as tg:
        for i in range(100):
            tg.start_soon(connent_ws)

anyio.run(main)