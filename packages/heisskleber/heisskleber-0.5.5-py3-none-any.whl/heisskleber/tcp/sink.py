import asyncio
from typing import Any, Callable

from heisskleber.core.types import AsyncSink, Serializable
from heisskleber.tcp.config import TcpConf


class AsyncTcpSink(AsyncSink):
    def __init__(self, config: TcpConf, pack: Callable):
        self.config = config
        self.reader: asyncio.StreamReader
        self.is_connected = False
        self.pack = pack

    def start(self) -> None:
        self.start_task = asyncio.create_task(self._connect())

    async def _connect(self) -> None:
        (_, self.writer) = await asyncio.open_connection(self.config.host, self.config.port)
        self.is_connected = True

    def stop(self) -> None:
        if self.is_connected:
            print("stopping")

    async def send(self, data: dict[str, Any], topic: str) -> None:
        payload = self.pack(data, topic)
        self.writer.write(payload)
