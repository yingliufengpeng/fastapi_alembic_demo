import anyio
import websockets

async def test_ws():
    uri = "ws://localhost:8000/ws/chat"
    async with websockets.connect(uri) as websocket:
        await websocket.send("Hello from client")
        response = await websocket.recv()
        print("收到消息:", response)

anyio.run(test_ws)
