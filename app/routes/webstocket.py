import anyio
import logging

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List

router = APIRouter()

_logger = logging.getLogger(__name__)

def safe_remove(self, conn):
    # 已经关闭，移除
    try:
        self.active_connections.remove(conn)
    except ValueError:
        pass

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
        safe_remove(self, websocket)

    async def broadcast(self, message: str):
        # 复制列表，避免迭代中修改
        async def b_impl(conn):
            try:
                await conn.send_text(message)
            except RuntimeError:
                # 已经关闭，移除
                safe_remove(self, conn)
            except Exception as e:
                print(f"广播异常: {e}", flush=True)
                safe_remove(self, conn)
        async with anyio.create_task_group() as tg:
            for conn in self.active_connections[:]:
                tg.start_soon(b_impl, conn)


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
    except Exception as e:
        print(f'xxxx', e)
        manager.disconnect(websocket)
        await manager.broadcast("某个用户离开了聊天室")