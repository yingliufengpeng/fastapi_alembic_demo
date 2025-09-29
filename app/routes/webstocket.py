import anyio
import logging

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List

router = APIRouter()

_logger = logging.getLogger(__name__)

# 管理 WebSocket 连接
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        # websocket.send_text(f'hello, world!')
        # _logger.info(f'new incoming ...')
        print(f'new incoming ...', flush=True)
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        async with anyio.create_task_group() as tg:
            for conn in self.active_connections:
                # tg.create_task(conn.send_text(message))
                tg.start_soon(conn.send_text, message)


manager = ConnectionManager()


@router.websocket("/ws/chat")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()  # 接收客户端消息
            await manager.broadcast(f"用户说: {data} from server")  # 广播给所有人
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast("某个用户离开了聊天室")
