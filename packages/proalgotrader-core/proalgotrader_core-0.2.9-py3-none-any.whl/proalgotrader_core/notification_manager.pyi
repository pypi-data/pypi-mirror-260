from _typeshed import Incomplete
from proalgotrader_core.algorithm import Algorithm as Algorithm
from typing import Any, Dict
from websockets import WebSocketClientProtocol as WebSocketClientProtocol

class NotificationManager:
    algorithm: Incomplete
    args_manager: Incomplete
    algo_session: Incomplete
    ws_url: Incomplete
    algo_session_key: Incomplete
    chat_url: Incomplete
    websocket: Incomplete
    task: Incomplete
    jobs: Incomplete
    def __init__(self, algorithm: Algorithm) -> None: ...
    async def connect(self) -> None: ...
    async def disconnect(self) -> None: ...
    async def run_websocket(self) -> None: ...
    def subscribe(self, topic: str) -> None: ...
    def send_message(self, topic: str, data: Dict[str, Any]) -> None: ...
