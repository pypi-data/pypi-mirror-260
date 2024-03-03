import asyncio
from typing import Callable

from heisskleber.core.types import Serializable
from heisskleber.tcp.config import TcpConf


class AsyncTcpConnection:
    """
    Async TCP connection, connects to host:port.
    """

    def __init__(self, config: TcpConf) -> None:
        self.config = config
        self.start_task: asyncio.Task[None] | None = None
        self.is_connected = asyncio.Event()

    def start(self) -> None:
        self.start_task = asyncio.create_task(self._connect())

    async def _check_connection(self) -> None:
        if not self.start_task:
            self.start()
        await self.is_connected.wait()

    async def _connect(self) -> None:
        print(f"{self} waiting for connection.")
        (self.reader, self.writer) = await asyncio.open_connection(self.config.host, self.config.port)
        print(f"{self} connected successfully!")
        self.is_connected.set()

    def stop(self) -> None:
        if self.is_connected:
            print("stopping")

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(host={self.config.host}, port={self.config.port})"
