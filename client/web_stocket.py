import anyio
import websockets

async def connent_ws():
    uri = "ws://localhost:8000/ws/chat"
    async with websockets.connect(uri) as websocket:
        await websocket.send("Hello from client")
        response = await websocket.recv()
        print("收到消息:", response)

anyio.run(connent_ws)
