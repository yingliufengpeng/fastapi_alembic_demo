# tests/test_websocket_sync.py
import logging
import anyio
import websockets
import unittest
from fastapi.testclient import TestClient
from app.app import app


logging.basicConfig(level=logging.INFO, force=True)
_logger = logging.getLogger(__name__)


class TestBasic(unittest.TestCase):

    def test_websocket(self):

        client = TestClient(app)
        _logger.info("开始测试")

        # 模拟 WebSocket
        with client.websocket_connect("/ws/chat") as ws:
            ws.send_text("Hello from test")
            data = ws.receive_text()
            print("收到消息:", data, flush=True)
            assert "Hello" in data






if __name__ == "__main__":
    unittest.main()



